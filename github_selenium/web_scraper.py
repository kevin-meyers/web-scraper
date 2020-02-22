from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TIMEOUT = 20


options = webdriver.ChromeOptions()
options.add_argument(' - incognito')

browser = webdriver.Chrome(
    executable_path='~/Downloads/chromedriver',
    chrome_options=options
)

def get_html(url):
    browser.get(url)
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((
                By.XPATH, '//img[@class="avatar width-full rounded-2"]'
            ))
        )

    except TimeoutException:
        print(“Timed out waiting for page to load”)
        browser.quit()
