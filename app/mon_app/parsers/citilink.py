import requests
from bs4 import BeautifulSoup
from mon_app.models import CompetitorProduct
import json
from decimal import Decimal


class HttpException(Exception):
    pass


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
    else:
        exp = HttpException()
        exp.status_code = r.status_code
        raise exp


def get_page_data(html):
    data_list = []
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='subcategory-product-item')

    for div in divs:
        json_product = div.get('data-params')
        url = div.find('a', class_='link_gtm-js link_pageevents-js ddl_product_link').get('href')
        data = json.loads(json_product)

        id_product = data.get('id')
        categoryId = data['categoryId']
        price = data['price']
        name = data['shortName']
        categoryName = data['categoryName']
        vendorName = data['brandName']
        shop = 'Ситилинк'

        data = {'id_product': id_product,
                'name': name,
                'price': price,
                'categoryId': categoryId,
                'categoryName': categoryName,
                'vendorName': vendorName.lower().title(),
                'url': url,
                'shop': shop}

        print(data)
        data_list.append(data)
    return data_list


def write_db(competitor_products):
    meta = {'updated_count': 0, 'created_count': 0}
    urls = [competitor_product.get('url') for competitor_product in competitor_products if competitor_product.get('url')]
    CompetitorProduct.objects.filter(url__in=urls).update(status=False)

    for competitor_product in competitor_products:
        url = competitor_product.get('url')

        if url:
            price = Decimal(competitor_product.get('price'))
            id_product = int(competitor_product.get('id_product'))
            categoryId = competitor_product.get('categoryId')
            categoryName = competitor_product.get('categoryName')
            vendorName = competitor_product.get('vendorName')
            groupId = competitor_product.get('groupId')
            shop = competitor_product.get('shop')
            name = competitor_product.get('name')

            _, created = CompetitorProduct.objects.update_or_create(url=url, defaults={'id_product': id_product,
                                                                                       'name': name,
                                                                                       'price': price,
                                                                                       'categoryId': categoryId,
                                                                                       'categoryName': categoryName,
                                                                                       'vendorName': vendorName,
                                                                                       'groupId': groupId,
                                                                                       'status': True,
                                                                                       'shop': shop})
            if created:
                meta['created_count'] += 1
            else:
                meta['updated_count'] += 1
    return meta


def citilink(url_target, page_count):
    pattern = url_target + '/?p={}'
    for i in range(1, int(page_count) + 1):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html)
        write_db(product_list)
        product_count_on_page = len(product_list)
        print("-" * 42)
        print("На странице номер {} получено {} продуктов".format(i, product_count_on_page))
        print("-" * 42)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')
    all_product_count = int(product_count_on_page) * int(page_count)
    print("Всего на странице {} получено {} продуктов".format(url_target, all_product_count))
    print("Парсинг завершен")
