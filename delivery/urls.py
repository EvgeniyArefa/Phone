from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.delivery, name = "delivery"),
]