from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

import speech_recognition as sr
import pyttsx3

search_engines = [
    {
        'name': 'Google',
        'url': 'https://www.google.com/',
        'input': 'q',
    },
    {
        'name': 'Bing',
        'url': 'https://www.bing.com/',
        'input': 'q',
    },
    {
        'name': 'DuckDuckGo',
        'url': 'https://duckduckgo.com/',
        'input': 'q',
    },
]


googleCookieDict = [
    {
        'name': '',
        'value': '',
        'domain': '.google.com'
    },
]


# 18% of organic clicks go to the first search result, 10% go to the second, and 7% go to the third.
# the first five organic results account for 67.60% of all the clicks


class Spartacus():
    def __init__(self):
        print("I am Sparticus!")
        self.driver = None
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')

    def go_to_link(self):
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.get("https://google.com")
        time.sleep(5)
        self.driver.quit()

    def query_search_engines(self, query_text):
        for engine in search_engines:

            self.driver = webdriver.Chrome(chrome_options=self.options)
            self.driver.get(engine['url'])
            # time.sleep(1)

            if engine['name'] == 'Google':
                elem = self.driver.find_element_by_name(engine['input'])
                self.load_google_cookies()
                elem.clear()
                elem.send_keys(query_text)
                elem.send_keys(Keys.RETURN)


                # figure out to handle modal...
                # modal = self.driver.find_element_by_tag_name("form")
                # button = modal.find_element_by_css_selector("[role = 'button']")
                # # print(butt)
                # button.click()

                links = self.driver.find_elements_by_link_text("Change to English")
                if elem in links:
                    print(elem)
                    # elem.click()
                time.sleep(20)

            get_google_responses(self.driver.page_source)

            time.sleep(3)
            self.driver.quit()

    def load_google_cookies(self):
        self.driver.add_cookie({
            'name': 'CONSENT',
            'value': 'YES+ES.es+V14+BX',
            'domain': '.google.com'
        })


def get_google_responses(page_source, limit=5):
    soup = BeautifulSoup(page_source, "html.parser")

    trigger = soup.findAll('a', href=True, text='Change to English')
    print(trigger)

    # First 5 Results
    search_results_by_limit = soup.find(id='rso').findChildren("div", {"class": "g"})[:limit]

    # Featured Snippets
    featured_snippet = soup.find_all(string="Images")
    print(featured_snippet)


def health():
    print("I am Spartacus!")
