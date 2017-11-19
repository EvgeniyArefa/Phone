from django.test import TestCase
from basket.views import separation, BasketListView


class SeparationTests(TestCase):

    def test_separation_main(self):
        """
        separation() returns a list of words that have been separat ";"
        """
        x = "first;123;second;4567;"
        self.assertQuerysetEqual(separation(x), ["'first'", "'123'", "'second'", "'4567'"])

    def test_separation_without_last_simbol(self):
        """
        separation() returns a list of words that have been separat ";"
        without last world if wasn't simbol ";" in end
        """
        x = "first;123;second;4567"
        self.assertQuerysetEqual(separation(x), ["'first'", "'123'", "'second'"])

    def test_separation_empty(self):
        """
        separation() returns an empty list if was nothing separats ";"
        """
        x = "first,123.second 4567_"
        self.assertQuerysetEqual(separation(x), [])

    def test_separation_empty_2(self):
        """
        separation() returns an empty list if was empty
        """
        x = ""
        self.assertQuerysetEqual(separation(x), [])


#class BasketListViewTests(TestCase):
    
#    def test_get_01(self):
#        x = BasketListView
#        self.assertQuerysetEqual(x.text, "К сожалению Ваша корзина пока что пуста")