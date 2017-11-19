from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from catalog.models import Good
from basket.models import Order
from django.db import connection
import datetime


def separation(zipp):
    result = []
    zipp_path = ""
    for char in zipp:
        if char == ";":
            if zipp_path:
                result.append(zipp_path)
                zipp_path = ""
            else:
                result.append(" ")
        else:
            zipp_path +=char
    return result


class BasketListView(ListView):
    template_name = 'basket/basket.html'
    model = Order
    text = None
    text_mas = []
    total = 0

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(status = 1)
            self.text = order.order_list
            self.text_mas = separation(self.text)
            self.total = order.reserve_3
        except:
            self.text = "К сожалению Ваша корзина пока что пуста"
        return super(BasketListView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(BasketListView, self).get_context_data(**kwargs)
        context["text"] = self.text
        context["text_mas"] = self.text_mas
        context["total"] = self.total
        return context


class OrderView(ListView):
    template_name = 'basket/basket.html'
    model = Order
    text = None
    text_order = None
    order = None

    def get(self, request, *args, **kwargs):
        try:
            self.order = Order.objects.exclude(status = 1)
        except:
            self.text_order = "К сожалению у Вас пока что нет заказов"
        return super(OrderView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context["order"] = self.order
        context["text"] = self.text
        context["text_order"] = self.text_order
        return context


class DelFirstView(BasketListView):

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(status = 1)
            self.text = order.order_list
            self.text_mas = separation(self.text)
            price = float(self.text_mas [5])
            self.text_mas = self.text_mas [6:]
            order.reserve_3 = order.reserve_3 - price
            if self.text_mas:
                i = 0
                y = 0
                for char in order.order_list:
                    i += 1
                    if char == ";":
                        y += 1
                    if y == 6:
                        break
                order.order_list = order.order_list[i:]
                order.save()
                self.total = order.reserve_3
            else:
                order.delete()
                self.text = "К сожалению Ваша корзина пока что пуста"
        except:
            self.text = "К сожалению Ваша корзина пока что пуста"
        return super(DelFirstView, self).get(request, *args, **kwargs)


class DelAllView(BasketListView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(status = 1)
        order.delete()
        self.text = "К сожалению Ваша корзина пока что пуста"
        return super(DelAllView, self).get(request, *args, **kwargs)


class DelLastView(BasketListView):

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(status = 1)
            self.text = order.order_list
            self.text_mas = separation(self.text)
            price = float(self.text_mas [-1])
            self.text_mas = self.text_mas [0:-6]
            order.reserve_3 = order.reserve_3 - price
            if self.text_mas:
                i = 0
                y = 0
                revers_list = reversed(order.order_list)
                for char in revers_list:
                    i += 1
                    if char == ";":
                        y += 1
                    if y == 7:
                        i -= 1
                        break
                order.order_list = order.order_list[0:-i]
                order.save()
                self.total = order.reserve_3
            else:
                order.delete()
                self.text = "К сожалению Ваша корзина пока что пуста"
        except:
            self.text = "К сожалению Ваша корзина пока что пуста"
        return super(DelLastView, self).get(request, *args, **kwargs)


class MakeOrderView(BasketListView):

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(status = 1)
            now = datetime.date.today()
            order.status = 2
            order.history = 'Оформлен' + ';' + str(now) + '.'
            order.save()
            self.text = "Заказ оформлен. Номер Вашаего заказа: " +\
            str(order.id)
        except:
            self.text = "К сожалению Ваша корзина пока что пуста"
        return super(BasketListView, self).get(request, *args, **kwargs)


class HistoryOrderView(DetailView):
    template_name = 'basket/history.html'
    model = Order
    pk_url_kwarg = "good_id"
    order = None
    id_order = None

    def get_context_data(self, **kwargs):
        context = super(HistoryOrderView, self).get_context_data(**kwargs)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM Order WHERE reserve_3 > 211000")
        row = cursor.fetchone()
        context["row"] = row
        return context

