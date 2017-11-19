import datetime

from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name = "Название")
    text = models.TextField(blank=True, verbose_name = "Описание")
    reserve = models.TextField(blank=True, verbose_name = "Резерв")
    
    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=100, verbose_name = "Название")
    code = models.PositiveIntegerField(unique = True, verbose_name = "Код")
    color = models.CharField(blank=True, max_length=50, verbose_name = "Цвет")
    text= models.TextField(verbose_name = "Описание")
    character_1 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 1")
    character_2 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 2")
    character_3 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 3")
    character_4 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 4")
    character_5 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 5")
    character_6 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 6")
    character_7 = models.CharField(max_length=50, blank=True, 
        verbose_name = "Характеристика 7")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
        verbose_name = "Категория")
    accessory = models.CharField(blank=True, max_length=50, 
        verbose_name = "Подкатегория")
    link = models.CharField(blank=True, max_length=500, 
        verbose_name = "Связь")
    pub = models.DateTimeField('date published')
    price = models.FloatField(verbose_name = "Цена, грн.")
    sale = models.PositiveSmallIntegerField(verbose_name = "Скидка, %", 
        default = 0)
    image = models.CharField(max_length=500, blank=True, 
        verbose_name = "Изображения")
    in_stock = models.BooleanField(default = True, 
        verbose_name = "Есть в наличии")
    score = models.PositiveIntegerField(default=0, verbose_name = "Балл")
    number = models.PositiveSmallIntegerField(default=0, 
        verbose_name = "Кол-во оценок")
    reserve_1 = models.TextField(blank=True, verbose_name = "Резерв 1")
    reserve_2 = models.CharField(blank=True, max_length=150, 
        verbose_name = "Резерв 2")
    reserve_3 = models.FloatField(blank=True, verbose_name = "Резерв 3")

    class Meta:
        ordering = ["-pub", "name"]

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub <= now
    was_published_recently.admin_order_field = 'pub'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Coment(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    autor = models.CharField(max_length=50) 
    text = models.TextField()
    pub = models.DateTimeField('date published')

    def __str__(self):
        return self.text