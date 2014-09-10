from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import unittest

class LogAShow(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    
    #Log in as a DJ
    def test_login(self):
        # TODO add this when we add users
        #browser.get('http://localhost:8000')
        sb = self.browser
        now = datetime.today()
        showdatein = now.strftime('%m/%d/%Y')
        showdateout = now.strftime('%Y-%m-%d')
        showtime = now.strftime('%H:%M:00')
        sb.get('http://localhost:8000/logger')
        self.assertIn('CHCR CRTC', self.browser.title)
        self.assertIn('Crazy Town Show',
            find_id(sb,'shows_list').text)
#        self.fail('Need to add users!')
        
        #Go to your own show
        show = find_link(sb, 'Show: Crazy Town Show Super Freak ()')
        show.click()

        #Create a new Episode
        self.assertIn('Crazy Town Show', sb.find_element_by_tag_name('h2').text)
        air_date = find_id(sb, 'id_air_date')
        air_time = find_id(sb, 'id_air_time')
        create_ep = find_id(sb, 'create_episode')
        air_date.send_keys(showdatein)
        air_time.send_keys(showtime)
        create_ep.click()
        ep_link = find_link(sb, 'Crazy Town Show (%s %s)' % (showdateout, showtime))
        ep_link.click()
        self.assertIn('Crazy Town Show (%s %s)' % (showdateout, showtime),
            sb.find_element_by_tag_name('h2').text)

        #Add Songs
        find_id(sb, 'new_Song').click()
        find_id(sb, 'id_time').send_keys('1:42')
        find_id(sb, 'id_title').send_keys('Hobo\'s Lullaby')
        find_id(sb, 'id_artist').send_keys('David Rovics')
        find_id(sb, 'id_composer').send_keys('Brahms')
        find_id(sb, 'id_length').send_keys('3:57')
        find_id(sb, 'play_Song').click()
        items = find_tags(sb, 'li')
        self.assertTrue( 
            any('Hobo' in it.text and '1:42' in it.text for it in items)
            )
        
        #TODO Should we just default to auto-entry or go to the same form we were at?
        #find_link(sb, 'Use Existing').click()
        tab = find_id(sb, 'Song')
        find_id(tab, 'id_time').send_keys('1:43')
        find_id(tab, 'id_Song_text').send_keys('H')
        sleep(2)
        find_id(tab,'id_Song_text').send_keys(Keys.DOWN + Keys.TAB)
        find_id(sb,'play_Song').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any('Hobo' in it.text and '1:43' in it.text for it in items)
            )

        #Add Ads
        find_link(sb, 'Advertisement').click()
        tab = find_id(sb, 'Advertisement')
        find_id(tab, 'new_Advertisement').click()
        find_id(tab, 'id_time').send_keys('1:44')
        find_id(tab, 'id_advertiser').send_keys('Alice\'s Chains')
        find_id(tab, 'id_length').send_keys('0:1:42')
        find_id(tab, 'play_Advertisement').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any('Alice' in it.text and '1:44' in it.text for it in items)
            )

        tab = find_id(sb, 'Advertisement')
        find_id(tab, 'id_time').send_keys('1:45')
        find_id(tab, 'id_Advertisement_text').send_keys('A')
        sleep(2)
        find_id(tab, 'id_Advertisement_text').send_keys(
            Keys.DOWN + Keys.TAB)
        find_id(tab, 'play_Advertisement').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any('Alice' in it.text and '1:45' in it.text for it in items)
            )

        #Add StationIDs
        find_link(sb, 'StationID').click()
        tab = find_id(sb, 'StationID')
        find_id(tab, 'new_StationID').click()
        find_id(tab, 'id_time').send_keys('1:46')
        find_id(tab, 'id_length').send_keys('0:0:42')
        find_id(tab, 'play_StationID').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any('STID' in it.text and '1:46' in it.text for it in items)
            )

        tab = find_id(sb, 'StationID')
        find_id(tab, 'id_time').send_keys('1:47')
        find_id(tab, 'id_StationID_text').send_keys('9')
        sleep(2)
        find_id(tab, 'id_StationID_text').send_keys(Keys.DOWN + Keys.TAB)
        find_id(tab, 'play_StationID').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any('STID' in it.text and '1:47' in it.text for it in items)
            )

        #Add Others
        find_link(sb, 'Other').click()
        tab = find_id(sb, 'Other')
        find_id(tab, 'new_Other').click()
        find_id(tab, 'id_time').send_keys('1:48')
        find_id(tab, 'id_description').send_keys('Talking crazy')
        find_id(tab, 'id_length').send_keys('0:1:42')
        find_id(tab, 'play_Other').click()
        items = find_tags(sb, 'li')
        self.assertTrue(
            any(' crazy' in it.text and '1:48' in it.text for it in items) 
            )

        tab = find_id(sb, 'Other')
        find_id(tab, 'id_time').send_keys('1:49')
        find_id(tab, 'id_Other_text').send_keys('c')
        sleep(2)
        find_id(tab, 'id_Other_text').send_keys(Keys.DOWN + Keys.TAB)
        find_id(tab, 'play_Other').click()
        items = find_tags(sb,'li')
        self.assertTrue(
            any(' crazy' in it.text and '1:49' in it.text for it in items) 
            )

 
    #Try to edit someone else's show (expect failure)

#Helper functions
def find_id(element, ident):
    return element.find_element_by_id(ident)

def find_link(element, link_text):
    return element.find_element_by_link_text(link_text)

def find_tags(element, tag):
    return element.find_elements_by_tag_name(tag)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
