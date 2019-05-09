from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt
from mon_app.models import MyProduct

import json


@csrf_exempt
def api_productmy_id(request, id):

    # ПОЛУЧИТЬ ТОВАР ПО id
    if request.method == "GET":
        product = MyProduct.objects.get(id=id)
        product_json = {"id": product.id,
                        "id_product": product.id_product,
                        "name": product.name,
                        "price": product.price,
                        "categoryId": product.categoryId,
                        "categoryName": product.categoryName,
                        "vendorName": product.vendorName,
                        "url": product.url,
                        "status": product.status,
                        "created": product.created
                        }
        return JsonResponse(product_json, safe=False)

    # ИЗМЕНИТЬ ТОВАР C УКАЗАННЫМ id
    if request.method == "PUT":
        product = MyProduct.objects.filter(id=id)
        new_product = json.loads(request.body)
        new_product_url = new_product.get('url')
        new_product_name = new_product.get('name')
        if new_product_url and new_product_name:
            updated = product.update(id_product=new_product('id_product'),
                                     name=new_product_name,
                                     price=new_product.get('price'),
                                     categoryId=new_product.get('categoryId'),
                                     categoryName=new_product.get('categoryName'),
                                     vendorName=new_product.get('vendorName'),
                                     url=new_product_url,
                                     status=new_product.get('status'),
                                     created=new_product.get('created')
                                     )
            updated_product = MyProduct.objects.get(id=id)
            return JsonResponse({"updated": updated,
                                 "id": updated_product.id,
                                 "id_product": updated_product.id_product,
                                 "name": updated_product.name,
                                 "price": updated_product.price,
                                 "categoryId": updated_product.categoryId,
                                 "categoryName": updated_product.categoryName,
                                 "vendorName": updated_product.vendorName,
                                 "url": updated_product.url,
                                 "status": updated_product.status,
                                 "created": updated_product.created
                                 }, safe=False)
        return JsonResponse({'err': True, 'message': 'Url or Name is lost'})

    # УДАЛИТЬ ТОВАР С УКАЗАННЫМ id
    if request.method == "DELETE":
        deleted_product = MyProduct.objects.get(id=id)
        deleted_product.delete()
        return JsonResponse({
            "deleted": 1,
            "id": deleted_product.id,
            "id_product": deleted_product.id_product,
            "name": deleted_product.name,
            "price": deleted_product.price,
            "categoryId": deleted_product.categoryId,
            "categoryName": deleted_product.categoryName,
            "vendorName": deleted_product.vendorName,
            "url": deleted_product.url,
            "status": deleted_product.status,
            "created": deleted_product.created
        })


@csrf_exempt
def api_productmy(request):

    # ДОБАВИТЬ НОВЫЙ ТОВАР
    if request.method == "POST":
        new_product = json.loads(request.body)
        new_product_url = new_product.get('url')
        new_product_name = new_product.get('name')
        if new_product_url and new_product_name:
            product, posted = MyProduct.objects.get_or_create(url=new_product_url,
                                                                                  defaults={'id_product': new_product.get('id_product'),
                                                                                            'name': new_product_name,
                                                                                            'price': new_product.get('price'),
                                                                                            'categoryId': new_product.get('categoryId'),
                                                                                            'categoryName': new_product.get('categoryName'),
                                                                                            'vendorName': new_product.get('vendorName'),
                                                                                            'status': new_product.get('status'),
                                                                                            'created': new_product.get('created')})
            return JsonResponse({"posted": posted,
                                 "id": product.id,
                                 "id_product": product.id_product,
                                 "name": product.name,
                                 "price": product.price,
                                 "categoryId": product.categoryId,
                                 "categoryName": product.categoryName,
                                 "vendorName": product.vendorName,
                                 "url": product.url,
                                 "status": product.status,
                                 "created": product.created
                                 }, safe=False)
        return JsonResponse({'err': True, 'message': 'Url or Name is lost'})

    # ПОЛУЧИТЬ ВСЕ ТОВАРЫ
    if request.method == "GET":
        products = MyProduct.objects.all()
        products_json = [{"id": product.id,
                          "id_product": product.id_product,
                          "name": product.name,
                          "price": product.price,
                          "categoryId": product.categoryId,
                          "categoryName": product.categoryName,
                          "vendorName": product.vendorName,
                          "url": product.url,
                          "status": product.status,
                          "created": product.created
                          }
                         for product in products]
        return JsonResponse(products_json, safe=False)
