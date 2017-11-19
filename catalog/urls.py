from django.conf.urls import url
from . import views
from catalog.views import GoodListView, GoodListCat, GoodDetailView, \
    GoodBuyView, SaleListView

app_name = 'catalog'
urlpatterns = [
    url(r'^$', GoodListView.as_view(), name = "catalog"),
    url(r'^sale$', SaleListView.as_view(), name = "sale"),
    url(r'catalog/price$', views.fil_price, name = "fil_price"),
    url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListCat.as_view(), 
        name = "catalog_id"),
    url(r'^(?P<prod_name>[\w+]+)$', views.prod_select, name='prod'),
    url(r'^acces/(?P<acces_name>[\w+]+)$', views.acces_select, name='acces'),
    url(r'^filter/(?P<filter_name>[\w+]+)$', views.filter, name='filter'),
    url(r'^good/(?P<good_id>\d+)/(?P<menu_name>[\w+]+)$', views.menu,
        name='menu'),
    url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name = "good"),
    url(r'^good/image/(?P<good_id>\d+)/(?P<image_side>[\w+]+)$', 
        views.image_select, name='image'),
    url(r'^buy/(?P<good_id>\d+)/$', GoodBuyView.as_view(), name = "buy"),
    url(r'^contacts$', views.contacts, name = "contacts"),
]