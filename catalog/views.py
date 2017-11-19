from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from catalog.models import Category, Good, Coment
from basket.models import Order
from django import forms

from django.http import HttpResponse

PRODUCT = None
ACCESSORY = None
CAT_ID = None
IMAGES_MASS = []
IMAGES_COUNT = 0
FILTER = '0'
MIN_PR = 0
MAX_PR = 1000000
GOOD_MENU = '1'
MESSAGE = ""
SALE = 0
CHARACTER_SMART = ['Диагональ экрана: ', 'Разрешение экрана: ', 'Камера: ',
                   'Количество ядер: ', 'Оперативная память: ',
                   'Внутренняя память: ']
CHARACTER_POWER = ['Аккумулятор: ', 'Гарантийный срок: ', 'Емкость, мАч: ',
                   'Выходной ток: ', 'Слотов зарядки: ', 'Особенности: ']
CHARACTER_ACCES = ['Хар-ка 1: ', 'Хар-ка 2: ', 'Хар-ка 3: ', 'Хар-ка 4: ', 
                    'Хар-ка 5: ', 'Хар-ка 6: ']
CHARACTER_HEAD = ['Тип наушников: ', 'Тип подключения: ', 'Назначение: ',
                   'Интерфейс проводного подключения: ', 'Тип крепления: ',
                   'Длина шнура, м: ']
CHARACTER_СOVER = ['Совместимая модель: ', 'Форм-фактор: ', 'Цвет: ']


class PriceFilterFrom(forms.Form):
    min_price = forms.FloatField
    max_price = forms.FloatField


def images_separation(image_in):
    result = []
    image_path = ""
    for char in image_in:
        if char == ";":
            if image_path:
                result.append(image_path)
                image_path = ""
        else:
            image_path +=char
    return result


class GoodListView(ListView):
    template_name = 'catalog/catalog.html'
    cat = None
    name_cat = None
    names_prod = None
    names_acces = None
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        global CAT_ID
        global IMAGES_COUNT
        global IMAGES_MASS
        global FILTER
        global MIN_PR
        global MAX_PR
        global GOOD_MENU
        SALE = 0
        GOOD_MENU = '1'
        IMAGES_COUNT = 0
        IMAGES_MASS = []
        if CAT_ID == None:
            self.cat = Category.objects.first()
            CAT_ID = self.cat
        else:
            self.cat = CAT_ID
        self.name_cat = Category.objects.all()
        if SALE == 0:
            self.names_prod = Good.objects.filter(category__name =\
                self.cat.name, price__gte = MIN_PR, price__lte = MAX_PR)
        else:
            self.names_prod = Good.objects.filter(category__name =\
                self.cat.name, price__gte = MIN_PR, price__lte = MAX_PR, 
                sale__gt = 0)
        self.names_acces = self.names_prod
        s = dict()
        for names_prod in self.names_prod:
            if names_prod.reserve_2 not in s:
                s[names_prod.reserve_2] = names_prod
        self.names_prod = s.values()
        s = dict()
        for names_acces in self.names_acces:
            if names_acces.accessory not in s:
                s[names_acces.accessory] = names_acces
        self.names_acces = s.values()
        return super(GoodListView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        context["category"] = self.cat
        context["name_cat"] = self.name_cat
        context["names_prod"] = self.names_prod
        context["names_acces"] = self.names_acces
        context["cat_name"] = str(CAT_ID)
        context["prod_name"] = PRODUCT
        context["acces_name"] = ACCESSORY
        context["filter_name"] = FILTER
        context["MIN_PR"] = MIN_PR
        context["MAX_PR"] = MAX_PR
        context["character"] = CHARACTER_SMART
        context["sale"] = SALE
        return context
    
    def get_queryset(self):
        global SALE
        SALE = 0
        if PRODUCT:
            results = Good.objects.filter(category = CAT_ID, 
                    reserve_2 = PRODUCT, price__gte = MIN_PR, 
                    price__lte = MAX_PR).order_by("name")
        elif ACCESSORY:
            results = Good.objects.filter(category = CAT_ID, 
                    accessory = ACCESSORY, price__gte = MIN_PR, 
                    price__lte = MAX_PR).order_by("name")
        else:
            results = Good.objects.filter(category = CAT_ID,
             price__gte = MIN_PR, price__lte = MAX_PR).order_by("name")
        if FILTER == '1':
            result = results.order_by("price")
        elif FILTER == '2':
            result = results.order_by("-price")
        elif FILTER == '3':
            result = results.order_by("-score")
        elif FILTER == '4':
            result = results.order_by("-pub")
        else:
            result = results
        return result


class SaleListView(GoodListView):

    def get(self, request, *args, **kwargs):
        global CAT_ID
        global IMAGES_COUNT
        global IMAGES_MASS
        global FILTER
        global MIN_PR
        global MAX_PR
        global GOOD_MENU
        SALE = 1
        GOOD_MENU = '1'
        IMAGES_COUNT = 0
        IMAGES_MASS = []
        if CAT_ID == None:
            self.cat = Category.objects.first()
            CAT_ID = self.cat
        else:
            self.cat = CAT_ID
        self.name_cat = Category.objects.all()
        if SALE == 0:
            self.names_prod = Good.objects.filter(category__name = 
                self.cat.name, price__gte = MIN_PR, price__lte = MAX_PR)
        else:
            self.names_prod = Good.objects.filter(category__name = 
                self.cat.name, price__gte = MIN_PR, price__lte = MAX_PR, 
                sale__gt = 0)
        self.names_acces = self.names_prod
        s = dict()
        for names_prod in self.names_prod:
            if names_prod.reserve_2 not in s:
                s[names_prod.reserve_2] = names_prod
        self.names_prod = s.values()
        s = dict()
        for names_acces in self.names_acces:
            if names_acces.accessory not in s:
                s[names_acces.accessory] = names_acces
        self.names_acces = s.values()
        return super(GoodListView, self).get(request, *args, **kwargs)
        
    def get_queryset(self):
        global SALE
        SALE = 1
        if PRODUCT:
            results = Good.objects.filter(category = CAT_ID, 
                    reserve_2 = PRODUCT, price__gte = MIN_PR, 
                    price__lte = MAX_PR, sale__gt = 0).order_by("name")
        elif ACCESSORY:
            results = Good.objects.filter(category = CAT_ID, 
                    accessory = ACCESSORY, price__gte = MIN_PR, 
                    price__lte = MAX_PR, sale__gt = 0).order_by("name")
        else:
            results = Good.objects.filter(category = CAT_ID,
            price__gte = MIN_PR, price__lte = MAX_PR, sale__gt = 0).\
            order_by("name")
        if FILTER == '1':
            result = results.order_by("price")
        elif FILTER == '2':
            result = results.order_by("-price")
        elif FILTER == '3':
            result = results.order_by("-score")
        elif FILTER == '4':
            result = results.order_by("-pub")
        else:
            result = results
        return result


class GoodListCat(GoodListView):

    def get(self, request, *args, **kwargs):
        global CAT_ID
        global PRODUCT
        global ACCESSORY
        global IMAGES_COUNT
        global IMAGES_MASS
        global FILTER
        global MIN_PR
        global MAX_PR
        global GOOD_MENU
        GOOD_MENU = '1'
        MIN_PR = 0
        MAX_PR = 1000000
        FILTER = '0'
        IMAGES_COUNT = 0
        IMAGES_MASS = []
        PRODUCT = None
        ACCESSORY = None
        self.cat = Category.objects.get(pk = self.kwargs["cat_id"])
        CAT_ID = self.cat
        self.name_cat = Category.objects.all()
        if SALE == 0:
            self.names_prod = Good.objects.filter(category__name =\
            self.cat.name,)
        else:
            self.names_prod = Good.objects.filter(category__name =\
            self.cat.name, sale__gt = 0)
        self.names_acces = self.names_prod
        s = dict()
        for names_prod in self.names_prod:
            if names_prod.reserve_2 not in s:
                s[names_prod.reserve_2] = names_prod
        self.names_prod = s.values()
        s = dict()
        for names_acces in self.names_acces:
            if names_acces.accessory not in s:
                s[names_acces.accessory] = names_acces
        self.names_acces = s.values()
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if SALE == 0:
            global SALE
            SALE = 0
            if PRODUCT:
                results = Good.objects.filter(category = CAT_ID, 
                        reserve_2 = PRODUCT, price__gte = MIN_PR, 
                        price__lte = MAX_PR).order_by("name")
            elif ACCESSORY:
                results = Good.objects.filter(category = CAT_ID, 
                        accessory = ACCESSORY, price__gte = MIN_PR, 
                        price__lte = MAX_PR).order_by("name")
            else:
                results = Good.objects.filter(category = CAT_ID,
                 price__gte = MIN_PR, price__lte = MAX_PR)\
                .order_by("name")
            if FILTER == '1':
                result = results.order_by("price")
            elif FILTER == '2':
                result = results.order_by("-price")
            elif FILTER == '3':
                result = results.order_by("-score")
            elif FILTER == '4':
                result = results.order_by("-pub")
            else:
                result = results
            return result
        else:    
            global SALE
            SALE = 1
            if PRODUCT:
                results = Good.objects.filter(category = CAT_ID, 
                        reserve_2 = PRODUCT, price__gte = MIN_PR, 
                        price__lte = MAX_PR, sale__gt = 0).\
                        order_by("name")
            elif ACCESSORY:
                results = Good.objects.filter(category = CAT_ID, 
                        accessory = ACCESSORY, price__gte = MIN_PR, 
                        price__lte = MAX_PR, sale__gt = 0).order_by\
                        ("name")
            else:
                results = Good.objects.filter(category = CAT_ID,
                 price__gte = MIN_PR, price__lte = MAX_PR, sale__gt = 0)\
                .order_by("name")
            if FILTER == '1':
                result = results.order_by("price")
            elif FILTER == '2':
                result = results.order_by("-price")
            elif FILTER == '3':
                result = results.order_by("-score")
            elif FILTER == '4':
                result = results.order_by("-pub")
            else:
                result = results
            return result


class GoodDetailView(DetailView):
    template_name = 'catalog/good.html'
    model = Good
    pk_url_kwarg = 'good_id'
    global IMAGES_COUNT
    global IMAGES_MASS
    global GOOD_MENU
    IMAGES_COUNT = 0
    IMAGES_MASS = []

    def get_context_data(self, **kwargs):
        global IMAGES_MASS
        global IMAGES_COUNT
        global CHARACTER_SMART
        global CHARACTER_POWER
        global CHARACTER_HEAD
        global CHARACTER_СOVER
        global MESSAGE
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        good_select = Good.objects.get(pk = self.kwargs["good_id"])
        good_select.score += 1
        good_select.save()
        image_mas = good_select.image
        images = images_separation(image_mas)
        IMAGES_MASS = images
        images_c = IMAGES_COUNT
        imagess = images[images_c]
        mes_error = MESSAGE
        MESSAGE = ""
        try:
            context["pn"] = self.request.GET["page"]
        except KeyError:
            context["pn"] = "1"
        context["cats"] = Category.objects.order_by("name")
        context["imagess"] = imagess
        context["GOOD_MENU"] = GOOD_MENU
        context["mes_error"] = mes_error
        if str(good_select.category) == 'Аксессуары':
            if good_select.accessory == 'PowerBank':
                context["character"] = CHARACTER_POWER
            elif good_select.accessory == 'Наушники':
                context["character"] = CHARACTER_HEAD
            else:
                context["character"] = CHARACTER_СOVER
        else:
            context["character"] = CHARACTER_SMART
        return context


class GoodBuyView(GoodDetailView):
    template_name = 'catalog/good_buy.html'
    model = Good
    pk_url_kwarg = 'good_id'

    def post(self, request, *args, **kwargs):
        global MESSAGE
        if request.method == "POST":
            try:
                good = Good.objects.get(pk = self.kwargs['good_id'])
                if good.sale > 0:
                    price = good.reserve_3
                else:
                    price = good.price
                sum = int(request.POST["count"])*price
                text = str(good.code) + ";" + str(good.name) + ";"\
                    + str(good.color) + ";" + str(request.POST["count"])\
                    + ";" + str(price) + ";" + str(sum) + ";"
                try:
                    order = Order.objects.get(status = 1)
                    order.order_list += text
                    order.reserve_3 += sum
                    order.save()
                    mes_error = "Товар добавлен в корзину!"
                except:
                    order = Order(order_list = text, status = 1, 
                        reserve_3 = sum, history = "Формируется")
                    order.save()
                    mes_error = "Товар добавлен в корзину!"
            except ValueError:
                mes_error = "Вы ввели не корректное значение!"
            MESSAGE = mes_error
        return super(GoodBuyView, self).get(request, *args, **kwargs)


def prod_select(request, prod_name):
    global PRODUCT
    global IMAGES_COUNT
    global IMAGES_MASS
    IMAGES_COUNT = 0
    IMAGES_MASS = []
    if prod_name != 'None':
        PRODUCT = prod_name
    else:
        PRODUCT = None
    if SALE == 0:
        links = "catalog:catalog_id"
    else:
        links = "catalog:sale"
    context = {
        'links': links,
    }
    return render(request, 'catalog/redirect.html', context)


def acces_select(request, acces_name):
    global ACCESSORY
    global IMAGES_COUNT
    global IMAGES_MASS
    IMAGES_COUNT = 0
    IMAGES_MASS = []
    if acces_name != 'None':
        ACCESSORY = acces_name
    else:
        ACCESSORY = None
    if SALE == 0:
        links = "catalog:catalog_id"
    else:
        links = "catalog:sale"
    context = {
        'links': links,
    }
    return render(request, 'catalog/redirect.html', context)


def image_select(request, good_id, image_side):
    global IMAGES_MASS
    global IMAGES_COUNT
    count = len(IMAGES_MASS)
    if image_side == 'right':
        if IMAGES_COUNT < (count - 1):
            IMAGES_COUNT += 1
        else:
            IMAGES_COUNT = 0
    if image_side == 'left':
        if IMAGES_COUNT > 0:
            IMAGES_COUNT -= 1
        else:
            IMAGES_COUNT = count - 1
    links = "catalog:good"
    context = {
        'links': links,
        'good_id': good_id,
    }
    return render(request, 'catalog/redirect.html', context)


def filter(request, filter_name):
    global FILTER
    if filter_name == '1':
        FILTER = '1'
    elif filter_name == '2':
        FILTER = '2'
    elif filter_name == '3':
        FILTER = '3'
    elif filter_name == '4':
        FILTER = '4'
    else:
        FILTER = '0'
    if SALE == 0:
        links = "catalog:catalog_id"
    else:
        links = "catalog:sale"
    context = {
        'links': links,
        'filter_name': filter_name,
    }
    return render(request, 'catalog/redirect.html', context)


def fil_price(request):
    global MIN_PR
    global MAX_PR
    mes_error = None
    if request.method == "POST":
        try:
            min_price = float(request.POST["min_price"])
            max_price = float(request.POST["max_price"])
            if min_price > max_price:
                mes_error = "Вы ввели минимальную цену больше, чем\
                максимальную"
            else:
                MIN_PR = min_price
                MAX_PR = max_price
        except ValueError:
            mes_error = "Вы ввели не корректное значение!"
    if SALE == 0:
        links = "catalog:catalog_id"
    else:
        links = "catalog:sale"    
    context = {
        'links': links,
    }
    return render(request, 'catalog/redirect.html', context)


def menu(request, good_id, menu_name):
    global GOOD_MENU
    if menu_name == '2':
        GOOD_MENU = '2'
    elif menu_name == '3':
        GOOD_MENU = '3'
    elif menu_name == '4':
        GOOD_MENU = '4'
    else:
        GOOD_MENU = '1'
    links = "catalog:good"
    context = {
        'links': links,
        'good_id': good_id,
    }
    return render(request, 'catalog/redirect.html', context)


def contacts(request):
    return HttpResponse('contacts form')


