# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_list', models.TextField(verbose_name='Описание заказа')),
                ('status', models.CharField(choices=[(1, 'Формируется'), (2, 'Оформлен'), (3, 'Обрабатывается'), (4, 'Отправлен'), (5, 'Оплачен'), (6, 'Получен'), (7, 'Возвращён'), (8, 'Отменён'), (9, 'Резерв')], max_length=15, verbose_name='Статус заказа')),
                ('history', models.TextField(verbose_name='История заказа')),
                ('user_name', models.CharField(blank=True, max_length=50, verbose_name='Имя пользователя')),
                ('user_email', models.EmailField(blank=True, max_length=254, verbose_name='Эл_почта пользователя')),
                ('reserve_1', models.TextField(blank=True, verbose_name='Резерв 1')),
                ('reserve_2', models.CharField(blank=True, max_length=150, verbose_name='Резерв 2')),
                ('reserve_3', models.FloatField(blank=True, verbose_name='Резерв 3')),
            ],
        ),
    ]