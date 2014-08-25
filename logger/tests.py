from selenium import webdriver
import unittest

class LogAShow(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def test_login(self):
        # TODO add this when we add users
        #browser.get('http://localhost:8000')

        self.browser.get('http://localhost:8000/logger')
        self.assertIn('CHCR CRTC', self.browser.title)
        self.fail('Need to add users!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
