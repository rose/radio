from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from logger.views import *

class HomePageTest(TestCase):

    pass
#    def test_root_url_goes_to_login_page(self):
#        found = resolve('/')
#        self.assertEqual(found.func, login)

class ShowsPageTest(TestCase):

    pass
#    def test_shows_page_url_resolves(self):
#        found = resolve('/logger/')
#        self.assertEqual(found.func, ListShowView.as_view())

#    def test_shows_page_returns_correct_html(self):
#        request = HttpRequest()
#        response = ListShowView.as_view()(request)
#        self.assertTrue(response.content.startswith(b'<html'))
