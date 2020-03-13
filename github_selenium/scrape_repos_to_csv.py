import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TIMEOUT = 20
GITHUB_IMG_CLASS='//img[@class="avatar width-full height-full avatar-before-user-status"]'
GITHUB_TITLE_CLASS='//a[@itemprop="name codeRepository"]'
GITHUB_LANGUAGE_CLASS='//span[@itemprop="programmingLanguage"]'

options = webdriver.ChromeOptions()
options.add_argument(' - incognito')

browser = webdriver.Chrome(
    executable_path=r'/home/kevin/Downloads/chromedriver',
    options=options
)

def get_html(url):
    browser.get(url)
    try:
        WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located((
                By.XPATH, GITHUB_IMG_CLASS
            ))
        )

    except TimeoutException:
        print('Timed out waiting for page to load')
        browser.quit()

    title_elements = browser.find_elements_by_xpath(
        GITHUB_TITLE_CLASS
    )

    titles = [x.text for x in title_elements]

    language_elements = browser.find_elements_by_xpath(
        GITHUB_LANGUAGE_CLASS
    )

    languages = [x.text for x in language_elements]

    return [(t, l) for t, l in zip(titles, languages)]


def make_url(user):
    return f'https://github.com/{user}?tab=repositories'


if __name__ == '__main__':
    with open('urls.txt') as f, open('output.csv', 'w') as o:
        headers = ['username', 'repo_name', 'most_used_language']
        csv_writer = csv.writer(o)
        csv_writer.writerow(headers)
        for username in f.readlines():
            username = username.strip()
            url = make_url(username)
            response_pairs = get_html(url)
            for title, language in response_pairs:
                csv_writer.writerow([username, title, language])
