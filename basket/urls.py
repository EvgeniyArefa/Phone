from django.conf.urls import url
from . import views
from basket.views import BasketListView, OrderView, DelFirstView, \
	DelLastView, DelAllView, MakeOrderView, HistoryOrderView


app_name = 'basket'
urlpatterns = [
    url(r'^$', BasketListView.as_view(), name = "basket"),
    url(r'^order$', OrderView.as_view(), name = "order"),
    url(r'^delfirst$', DelFirstView.as_view(), name = "delfirst"),
    url(r'^delall$', DelAllView.as_view(), name = "delall"),
    url(r'^dellast$', DelLastView.as_view(), name = "dellast"),
    url(r'^makeorder$', MakeOrderView.as_view(), name = "makeorder"),
    url(r'^history/(?P<good_id>\d+)$', HistoryOrderView.as_view(), 
    	name = "history"),
]
