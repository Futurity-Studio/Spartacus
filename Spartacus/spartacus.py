from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FFOptions
from webdriver_manager.chrome import ChromeDriverManager
import re
from functools import reduce


search_engines = [
    {
        'name': 'Google',
        'url': 'https://www.google.com/',
        'input': 'q',
    },
    # {
    #     'name': 'Bing',
    #     'url': 'https://www.bing.com/',
    #     'input': 'q',
    # },
    # {
    #     'name': 'DuckDuckGo',
    #     'url': 'https://duckduckgo.com/',
    #     'input': 'q',
    # },
]

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

class Spartacus:
    def __init__(self):
        print("I am Sparticus!")
        self.driver = None
        self.options = None
        self.unified_response = ''

    # todo -- add support for DuckDuckGo
    # todo -- add support for Bing
    # todo -- add support for firebase <> cookie modules
    # todo -- create nodejs express server to interface cookies
    # todo -- create conceptual smart contract process for paying people for their cookies
    # todo -- add packet sniffing... 🙃

    def go_to_link(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=self.options)
        self.driver.get("https://google.com")
        time.sleep(5)
        self.driver.quit()

    def go_to_link_ff(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.driver.get("https://google.com")
        time.sleep(5)
        self.driver.quit()


    def query_search_engines_GC(self, query_text):
        for engine in search_engines:

            self.driver = webdriver.Chrome(chrome_options=self.options)
            self.driver.get(engine['url'])
            # time.sleep(1)

            if engine['name'] == 'Google':
                time.sleep(1)
                elem = self.driver.find_element_by_name(engine['input'])
                self.load_google_cookies()
                elem.clear()
                elem.send_keys(query_text)
                elem.send_keys(Keys.RETURN)
                self.get_google_responses()

            time.sleep(3)
            self.driver.quit()
            return self.unified_response


    def query_search_engines_FF(self, query_text):
        for engine in search_engines:
            self.options = FFOptions()
            self.options.headless = True
            self.driver = webdriver.Firefox(options=self.options, executable_path=GeckoDriverManager().install())
            self.driver.get(engine['url'])
            # time.sleep(1)

            if engine['name'] == 'Google':
                time.sleep(1)
                elem = self.driver.find_element_by_name(engine['input'])
                self.load_google_cookies()
                elem.clear()
                elem.send_keys(query_text)
                elem.send_keys(Keys.RETURN)
                time.sleep(1)
                self.get_google_responses()

            time.sleep(3)
            self.driver.quit()
            return self.unified_response

    def unify_response(self, responses):
        """
        todo -- something magical happens here...
            some examples:

        """
        prices_strings = []
        regex = re.compile(r'\$(\d?[\d.,]*\b)')
        for s in responses:
            print(s)
            prices_strings.append([x.replace(',', '') for x in re.findall(regex, s)])

        prices_strings = [item for sublist in prices_strings for item in sublist]
        prices_strings_clean = filter(len, prices_strings)
        prices_strings_float = [float(p) for p in prices_strings_clean]

        exchange_rate = .82
        mean_price = round( reduce(lambda a, b: a + b, prices_strings_float) / len(prices_strings_float) * exchange_rate, 2)
        print(mean_price)

        # set single response as class variable... (useful for more than one data source)
        self.unified_response = f'{mean_price} euro'

    def load_google_cookies(self):
        for cookie in google_cookie_dict:
            self.driver.add_cookie(cookie)

    def get_google_responses(self, limit=5):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # trigger = soup.findAll('a', href=True, text='Change to English')
        # print(trigger)

        # First 5 Results
        # search_results_by_limit = soup.find(id='rso').findChildren("div", {"class": "rc"})[:limit]
        # # print(search_results_by_limit)
        # print(len(search_results_by_limit))
        # for search_result in search_results_by_limit:
        #     result_text = search_result.get_text()
        #     print(result_text)

        # Featured Snippets
        featured_response_texts = []
        featured_snippets = soup.find_all('h2', string="Featured snippet from the web")
        for featured_snippet in featured_snippets:
            sibling = featured_snippet.find_next_sibling()
            featured_response_text = sibling.contents[0].get_text()
            # print(featured_response_text)
            featured_response_texts.append(featured_response_text)


        query_responses = []
        for g in soup.find_all(class_='g'):
            # print(g.text)
            query_responses.append(g.text)
        # print(query_responses)

        self.unify_response(query_responses)


def health():
    print("I am Spartacus!")
