from django.test import TestCase
from catalog.models import Good, Category
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db import models


class GoodListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        cat = Category.objects.create(name='Смартфон', id = 1)
        number_of_goods = 13
        for good_num in range(number_of_goods):
            good = Good.objects.create(id = good_num, name='Telephone %s' 
            % good_num, code=good_num, text = 'Text %s' % good_num, pub=now, 
            price=100+good_num, sale=0, in_stock=True, score=0, number=0, 
            reserve_3=0, category = cat)


    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/'+'?page=4')
        self.assertEqual(resp.status_code, 200)
        #self.assertTrue('is_paginated' in resp.context)
        #self.assertTrue(resp.context['page_obj.number'], True)
        #self.assertTrue( resp.context['paginate_by'], 10)

    #def test_view_url_accessible_by_name(self):
    #    resp = self.client.get(reverse('/catalog/catalog/'))
    #    self.assertEqual(resp.status_code, 200)