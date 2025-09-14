#%%
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from get_books import BasePage, Urls, get_driver


class RiskListSchema:
    HREF_LINK = 'href_link'
    TITLE = 'title'


class OWASPTop10Page(BasePage):
    # Locators
    RISK_LIST = (
        By.CSS_SELECTOR, 
        '#sec-main p:has(+#top-10-web-application-security-risks) ~ ul li'
        )
    RESULT_FILE_NAME = 'owasp_top_10.csv'

    def __init__(self, driver: WebDriver):
        super().__init__(driver, Urls.OWASP_TOP_10_URL)

    def get_risk_list(self):
        risk_list = self.find_elements(self.RISK_LIST)
        return [
            {
                RiskListSchema.HREF_LINK: risk.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                RiskListSchema.TITLE: risk.find_element(By.TAG_NAME, 'strong').text
                } for risk in risk_list
            ]


#%% Task 6: Scraping Structured Data
def fetch_top_10_risks():
    with get_driver() as driver:
        page = OWASPTop10Page(driver)
        page.open_main_page()
        risk_list = page.get_risk_list()
        page.write_csv(page.RESULT_FILE_NAME, risk_list, [
            RiskListSchema.HREF_LINK, 
            RiskListSchema.TITLE
            ])

#%%
fetch_top_10_risks()

#%%
