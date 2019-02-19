from .models import *
import datetime
import pylab


def status_true_util(modeladmin, request, queryset):
    rows_updated = queryset.update(status='True')
    if rows_updated == 1:
        message_bit = "1 Competitor`s products was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as True." % message_bit)


def status_false_util(modeladmin, request, queryset):
    rows_updated = queryset.update(status='False')
    if rows_updated == 1:
        message_bit = "1 Competitor`s product was"
    else:
        message_bit = "%s Competitor`s products were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as False." % message_bit)


def start_matching_competitor_util(modeladmin, request, queryset):
    products_competitor = queryset.values('id_product', 'name', 'price', 'shop', 'url')

    for product_competitor in products_competitor:
        shop_competitor = product_competitor.get('shop')
        id_product_competitor = product_competitor.get('id_product')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')
        url_competitor = product_competitor.get('url')

        product_my = MyProduct.objects.filter(id_product=id_product_competitor).values('id_product', 'name', 'price')[0]
        id_product_my = product_my.get('id_product')
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        diff = price_my - price_competitor

        if diff < 0:
            status = True
        elif diff > 0:
            status = False
        else:
            status = None

        Match.objects.update_or_create(id_product=id_product_competitor,
                                       defaults={'id_product': id_product_my,
                                                 'name_my': name_my,
                                                 'price_my': price_my,
                                                 'shop_competitor': shop_competitor,
                                                 'name_competitor': name_competitor,
                                                 'url': url_competitor,
                                                 'price_competitor': price_competitor,
                                                 'diff': diff,
                                                 'status': status
                                                 })
    modeladmin.message_user(request, "Объекты сравнены")


def start_matching_my_util(modeladmin, request, queryset):
    products_my = queryset.values('id_product', 'name', 'price')

    for product_my in products_my:
        id_product_my = product_my.get('id_product')
        name_my = product_my.get('name')
        price_my = product_my.get('price')

        product_competitor = CompetitorProduct.objects.filter(id_product=id_product_my).values('shop', 'id_product', 'name', 'price')[0]
        shop_competitor = product_competitor.get('shop')
        id_product_competitor = product_competitor.get('id_product')
        name_competitor = product_competitor.get('name')
        price_competitor = product_competitor.get('price')

        diff = price_my - price_competitor

        if diff < 0:
            status = True
        elif diff > 0:
            status = False
        else:
            status = None

        Match.objects.update_or_create(id_product=id_product_my,
                                       defaults={'id_product': id_product_competitor,
                                                 'name_my': name_my,
                                                 'price_my': price_my,
                                                 'shop_competitor': shop_competitor,
                                                 'name_competitor': name_competitor,
                                                 'price_competitor': price_competitor,
                                                 'diff': diff,
                                                 'status': status
                                                 })
    modeladmin.message_user(request, "Объекты сравнены")


def save_graph_util(modeladmin, request, queryset):
    products = queryset.values('shop_competitor', 'price_my', 'price_competitor', 'name_my')
    for product in products:
        shops = product.get('shop_competitor')
        price_my = product.get('price_my')
        price_competitor = product.get('price_competitor')
        name = product.get('name_my')

        data_my = {'name': name,
                   'price': price_my}

        data_competitor = {"shops": shops,
                           'price': price_competitor,
                           'name': name}

    pylab.savefig('mon_app/graphs/match_' + str(datetime.datetime.now()).replace(' ', '') + '.png')
