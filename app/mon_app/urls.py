from django.urls import path

from mon_app.api.competitor_products_api import api_productcompetitor_id, api_productcompetitor
from mon_app.api.my_products_api import api_productmy_id, api_productmy
from mon_app.api.match_api import api_match_id, api_match
from .views import index, parsing, support, other


urlpatterns = [
    path('', index, name='index_url'),
    path('parsing/', parsing, name='parsing_url'),
    path('support/', support, name='support_url'),
    path('other/', other, name='other_url'),
    path('api/productcompetitor/<id>', api_productcompetitor_id, name='api_productcompetitor_id_url'),
    path('api/productcompetitor/', api_productcompetitor, name='api_productcompetitor_url'),
    path('api/productmy/<id>', api_productmy_id, name='api_productmy_id_url'),
    path('api/productmy/', api_productmy, name='api_productmy_url'),
    path('api/match/<id>', api_match_id, name='api_match_id_url'),
    path('api/match/', api_match, name='api_match_url')
]
