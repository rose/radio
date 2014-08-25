from django.core.urlresolvers import resolve
from django.test import TestCase
from logger.views import *

class HomePageTest(TestCase):

    def test_root_url_goes_to_login_page(self):
        found = resolve('/')
        self.assertEqual(found.func, login)

