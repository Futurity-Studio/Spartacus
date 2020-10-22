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


# {
#     'name': '',
#     'value': '',
#     'domain': '.google.com'
# },

google_cookie_dict = [
    {
        'name': 'CONSENT',
        'value': 'YES+ES.es+V14+BX',
        'domain': '.google.com'
    },
    {
        'name': 'CGIC',
        'value': 'IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45',
        'domain': '.google.com'
    },
    {
        'name': '1P-JAR',
        'value': '2020-10-22-12',
        'domain': '.google.com'
    },
    {
        'name': 'NID',
        'value': '204=Z9hccyZGL8V0peRLI966PZfrpOsgC8-pBBxoBG6_2oBD-nvIR_umPzdYEGjzmEs8JoK9O88HX6M6P4sYwtlecUAemvPxmD10ikycEABYXDMJuHA0g5G8CA_wf0jqf0cqhfpLAuXZiuJbW0p_4QOEMeAqDpldDFb4ehoY6fGbx9I',
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
        for cookie in google_cookie_dict:
            self.driver.add_cookie(cookie)


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
