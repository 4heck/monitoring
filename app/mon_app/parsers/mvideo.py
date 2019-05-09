import requests
from bs4 import BeautifulSoup
from mon_app.models import CompetitorProduct
import random
from decimal import Decimal, InvalidOperation


def get_html(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
    print(r.status_code)


def refined(s):
    s1 = s.replace('\t', '')
    s2 = s1.replace('\n', '')
    s3 = s2.replace('\r', '')
    return s3


def get_page_data(html):
    data_list = []
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('a', class_="sel-product-tile-title")

    for div in divs:
        url = 'https://www.mvideo.ru' + div.get('href')
        products = div.get('data-product-info').split('{')[1::2]

        for product in products:
            refined_product = refined(product)
            p = '{' + refined_product

            d = eval(p)

            id_product = d.get('productId')
            name = d.get('productName')
            price = d.get('productPriceLocal')
            categoryId = d.get('productCategoryId')
            categoryName = d.get('productCategoryName')
            vendorName = d.get('productVendorName')
            groupId = d.get('productGroupId')
            shop = 'М.видео'

            data = {'id_product': id_product,
                    'name': name,
                    # генерация цены с рандомайзером для создания образца базы данных МОИХ товаров
                    'price': float(price) + round(random.uniform(-1, 1)*400)*5,
                    # 'price': price;
                    'categoryId': categoryId,
                    'categoryName': categoryName,
                    'vendorName': vendorName.lower().title(),
                    'groupId': groupId,
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
            try:
                price = Decimal(competitor_product.get('price'))
            except InvalidOperation:
                price = None
            try:
                id_product = int(competitor_product.get('id_product'))
            except ValueError:
                id_product = None

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


def mvideo(url_target, page_count):
    pattern = url_target + '/f/page={}'
    for i in range(1, int(page_count) + 1):
        url = pattern.format(str(i))
        html = get_html(url)
        product_list = get_page_data(html)
        write_db(product_list)
        product_count_on_page = len(product_list)
        print("-" * 42 + "\nНа странице номер {} получено {} продуктов".format(i, product_count_on_page) + "\n" + "-" * 42)
        meta = write_db(product_list)
        print(f'--> {i}: {meta}')
    all_product_count = int(product_count_on_page) * int(page_count)
    print("-" * 42 + "\nВсего на странице {} получено {} продуктов".format(url_target, all_product_count) + "\n" + "-" * 42)
