#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from contextlib import contextmanager
import pandas as pd
import re
import json
import csv


class Urls:
    # URLs
    DCL_ROBOTS_URL = 'https://durhamcountylibrary.org/robots.txt'
    DCL_SEARCH_URL = 'https://durhamcounty.bibliocommons.com/'
    DCL_PREMADE_SEARCH_URL = 'https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart'
    WP_ROBOTS_URL = 'https://en.wikipedia.org/robots.txt'
    OWASP_TOP_10_URL = 'https://owasp.org/www-project-top-ten/'


class BasePage:
    DEFAULT_WAIT_TIMEOUT = 10
    DEFAULT_SHORT_WAIT_TIMEOUT = 4

    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url

    def _wait_for(self, timeout, condition, *args):
        try:
            return WebDriverWait(self.driver, timeout).until(condition(*args))
        except TimeoutException:
            raise

    def open_main_page(self):
        self.driver.get(self.url)
        return self

    def open_url(self, url: str):
        self.driver.get(url)
        return self

    def get_source(self):
        return self.driver.page_source

    def wait_for_element(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        return self._wait_for(timeout, EC.presence_of_element_located, locator)

    def wait_for_elements(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        try:
            return self._wait_for(timeout, EC.presence_of_all_elements_located, locator)
        except TimeoutException:
            return []

    def is_present(self, locator, timeout=DEFAULT_WAIT_TIMEOUT):
        try:
            return bool(WebDriverWait(self.driver, timeout)
                        .until(EC.presence_of_element_located(locator)))
        except Exception:
            return False

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.find_element(locator).click()

    def verify_selenium_allowed(self):
        robots_txt = self.get_source()
        return 'selenium' in robots_txt.lower()

    # File Handling functions
    def write_json(self, file_name, results):
        with open(file_name, 'w') as json_file:
            json.dump(results, json_file, indent=4)
        print(f'JSON file is written to {file_name}')

    def write_csv(self, file_name, data, header):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in data:
                writer.writerow(row[head] for head in header)
        print(f'CSV file is written to {file_name}')


class DurhamCountyLibraryPage(BasePage):
    # Locators
    ITEM_CARD_LIST = (By.CSS_SELECTOR, '.cp-search-result-item')
    ITEM_TITLE = (By.CSS_SELECTOR, '.title-content')
    ITEM_AUTHOR = (By.CSS_SELECTOR, '.author-link')
    ITEM_PRIMARY_INFO = (By.CSS_SELECTOR, '.display-info-primary')
    SEARCH_FIELD = (By.CSS_SELECTOR, '#desktop_search_form .main_search_input')
    PAGINATION_LABEL = (By.CSS_SELECTOR, '.result-controls .cp-pagination-label')
    NEXT_PAGE_CHEVRON_ACTIVE = (
        By.CSS_SELECTOR, 
        '.result-controls .pagination__desktop-items .cp-pagination-item.pagination__next-chevron'
        )
    NEXT_PAGE_CHEVRON_DISABLED = (
        By.CSS_SELECTOR, 
        '.result-controls .pagination__desktop-items .cp-pagination-item.pagination__next-chevron.pagination-item--disabled'
        )
    PAGE_CONTENT_INACTIVE = (By.CSS_SELECTOR, '.result-content.inactive')
    PAGE_CONTENT_ACTIVE = (By.CSS_SELECTOR, '.result-content.active')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '#desktop_search_form .input-group-btn button')
    LOAD_BAR_ACTIVE = (By.CSS_SELECTOR, '.cp-progress-bar .bar.active')
    LOAD_BAR_INACTIVE = (By.CSS_SELECTOR, '.cp-progress-bar .bar:not(.active)')
    LAST_ELEMENT_LOADED = (By.CSS_SELECTOR, '.cp-search-result-item:last-of-type:not(.fade-exit-active)')
    
    LANGUAGE_SEPARATOR = '—'
    RESULT_FILE_NAME = 'get_books.json'

    def __init__(self, driver: WebDriver):
        self.DCL_ROBOTS_URL = Urls.DCL_ROBOTS_URL
        self.DCL_SEARCH_URL = Urls.DCL_SEARCH_URL
        self.DCL_PREMADE_SEARCH_URL = Urls.DCL_PREMADE_SEARCH_URL
        super().__init__(driver, self.DCL_ROBOTS_URL)

    # Base functions
    def open_search_url(self):
        self.open_url(self.DCL_SEARCH_URL)
        return self

    def open_premade_search_url(self):
        self.open_url(self.DCL_PREMADE_SEARCH_URL)
        return self

    # Search and Results
    def search_books(self, query: str):
        ttt = self.find_element(self.SEARCH_FIELD)
        ttt.send_keys(query)
        self.click(self.SEARCH_BUTTON)
        return self

    def get_book_list(self):
        return self.find_elements(self.ITEM_CARD_LIST)

    def get_book_title(self, item_card: WebElement):
        return item_card.find_element(*self.ITEM_TITLE).text or None

    def get_author_list(self, item_card: WebElement):
        author_list = item_card.find_elements(*self.ITEM_AUTHOR)
        return None if not len(author_list) else author_list[0].text if len(author_list) == 1 else ';'.join(author.text for author in author_list)

    def get_format(self, item_card: WebElement):
        primary_info = item_card.find_element(self.ITEM_PRIMARY_INFO).text
        return primary_info.split(',')[0].strip() if primary_info else None

    def get_year(self, item_card: WebElement):
        primary_info = item_card.find_element(self.ITEM_PRIMARY_INFO).text
        return primary_info.split(',')[1].split(self.LANGUAGE_SEPARATOR)[-1].strip() if primary_info else None

    def get_format_year(self, item_card: WebElement):
        primary_info = item_card.find_element(*self.ITEM_PRIMARY_INFO).text
        return primary_info.split(self.LANGUAGE_SEPARATOR)[0].strip() if primary_info else None

    def get_book_info(self, item_card: WebElement) -> dict:
        return {
            'Title': self.get_book_title(item_card),
            'Author': self.get_author_list(item_card),
            'Format-Year': self.get_format_year(item_card)
            }

    # Pagination
    def get_total_pages(self, results_per_page=20):
        pagination_text = self.wait_for_element(self.PAGINATION_LABEL).text.lower()
        try:
            match = re.search(r'.*\s(\d+)\s*result|s', pagination_text)
            if not match:
                raise ValueError('No match found in pagination text')
            total_results = int(match.group(1))
            total_pages = (total_results // results_per_page + 1)
            print(f'Found {total_pages} pages')
            return total_pages
        except Exception as e:
            print(e)
            return None

    def wait_search_result_load_complete(self):
        try:
            self.wait_for_element(self.LOAD_BAR_ACTIVE, self.DEFAULT_SHORT_WAIT_TIMEOUT)
            self.wait_for_element(self.LOAD_BAR_INACTIVE, self.DEFAULT_SHORT_WAIT_TIMEOUT)
        except Exception:
            print('Loading bar wait timeout')
        self.wait_for_element(self.LAST_ELEMENT_LOADED, self.DEFAULT_SHORT_WAIT_TIMEOUT)

    def get_all_search_results_pagination(self):
        results = []
        disabled_next_page = []
        while not len(disabled_next_page):
            book_list = self.get_book_list()
            results.extend([self.get_book_info(card) for card in book_list])
            
            disabled_next_page = self.find_elements(self.NEXT_PAGE_CHEVRON_DISABLED)
            if not len(disabled_next_page):
                self.click(self.NEXT_PAGE_CHEVRON_ACTIVE)
                self.wait_search_result_load_complete()
        return results


class WikipediaRobotsPage(BasePage):
    def __init__(self, driver: WebDriver):
        self.WP_ROBOTS_URL = Urls.WP_ROBOTS_URL
        super().__init__(driver, self.WP_ROBOTS_URL)


# Driver Setup
@contextmanager
def get_driver(browser='chrome', headless=True):
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        # options.page_load_strategy = 'eager' # waits until DOMContentLoaded event fire is returned
        if headless:
            options.add_argument('--headless')  # Enable headless mode
        options.add_argument('--disable-gpu')  # Optional, recommended for Windows
        options.add_argument('--window-size=1920,1080')  # Optional, set window size
        driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        # options.page_load_strategy = 'normal'
        if headless:
            options.add_argument('--headless')  # Enable headless mode
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        driver = webdriver.Firefox(options=options)
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')  # Enable headless mode
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f'Unsupported browser: {browser}')
    try:
        yield driver
    finally:
        driver.quit()


#%% Task 3: Write a Program to Extract this Data
def get_books_info():
    with get_driver() as driver:
        page = DurhamCountyLibraryPage(driver)
        page.open_main_page()
        
        # Task 1 Review robots.txt to Ensure Policy Compliance
        if page.verify_selenium_allowed():
            print('Selenium Crawling is not allowed')
            return None
        
        # Task 2: Understanding HTML and the DOM for the Durham Library Site
        page.open_premade_search_url()
        page.wait_search_result_load_complete()
        book_list = page.get_book_list()
        results = [page.get_book_info(card) for card in book_list]
        return pd.DataFrame(results)

#%%
print(get_books_info())

#%% Task 3 (Optional): Write a Program to Extract Each Page
def get_all_pages_books_info():
    with get_driver() as driver:
        page = DurhamCountyLibraryPage(driver)
        page.open_main_page()
        if page.verify_selenium_allowed():
            print('Selenium Crawling is not allowed')
            return None

        page.open_search_url()
        page.search_books('spanish for beginner learn')
        page.wait_search_result_load_complete()
        total_found_pages = page.get_total_pages()
        if total_found_pages is None:
            print('Failed to retrieve total pages')
            return None
        elif total_found_pages == 1:
            book_list = page.get_book_list()
            results = [page.get_book_info(card) for card in book_list]
            return pd.DataFrame(results)

        # Task 4: Write out the Data
        results = page.get_all_search_results_pagination()
        page.write_json(page.RESULT_FILE_NAME, results)
        
        return pd.DataFrame(results) if results else None

#%% # Task 4: Write out the Data
df = get_all_pages_books_info()
df.to_csv('get_books.csv', index=False)

#%%
