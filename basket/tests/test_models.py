from django.test import TestCase

from basket.models import Order

class OrderModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Order.objects.create(order_list='IPhone6', status=1, 
            history='Формируется', reserve_3=15000, user_name='David')

    def test_order_list_label(self):
        order=Order.objects.get(id=1)
        field_label = order._meta.get_field('order_list').verbose_name
        self.assertEquals(field_label,'Описание заказа')

    def test_user_name_max_lenght(self):
        order=Order.objects.get(id=1)
        max_length = order._meta.get_field('user_name').max_length
        self.assertEquals(max_length,50)

    def test_order__str__(self):
        order=Order.objects.get(id=1)
        self.assertEquals(order.__str__(),'IPhone6')