from django.db import models


class Order(models.Model):
    Stat_cho = ((1, "Формируется"), (2, "Оформлен"), (3, "Обрабатывается"),
        (4, "Отправлен"), (5, "Оплачен"), (6, "Получен"), (7, "Возвращён"), 
        (8, "Отменён"), (9, "Резерв"))
    order_list = models.TextField(verbose_name = "Описание заказа")
    status = models.IntegerField(choices=Stat_cho, 
        verbose_name = "Статус заказа")
    history = models.TextField(verbose_name = "История заказа")
    user_name = models.CharField(blank=True, max_length=50, 
        verbose_name = "Имя пользователя")
    user_email = models.EmailField(blank=True, 
        verbose_name = "Эл_почта пользователя")
    reserve_1 = models.TextField(blank=True, verbose_name = "Резерв 1")
    reserve_2 = models.CharField(blank=True, max_length=150, 
        verbose_name = "Резерв 2")
    reserve_3 = models.FloatField(blank=True, verbose_name = "Резерв 3")

    def __str__(self):
        return self.order_list