from selenium import webdriver
import unittest

class LogAShow(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    
    #Log in as a DJ
    def test_login(self):
        # TODO add this when we add users
        #browser.get('http://localhost:8000')

        self.browser.get('http://localhost:8000/logger')
        self.assertIn('CHCR CRTC', self.browser.title)
        self.fail('Need to add users!')
        
    #Go to your own show

    #Create a new Episode

    #Add new segments to it

    #Add existing segments to it (Won't work until users created)

    #Try to edit someone else's show (expect failure)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
