# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help='Choose browser: chrome or firefox')
    parser.addoption('--language', action='store', default='en',
                     help='Choose language: en, ru, fr, etc.')


@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption('browser_name')
    user_language = request.config.getoption('language')
    browser = None

    if browser_name == 'chrome':
        print('\nStart chrome browser for test..')
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})

        # Современные настройки Chrome
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        browser = webdriver.Chrome(options=options)
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    elif browser_name == 'firefox':
        print('\nStart firefox browser for test..')
        options = FirefoxOptions()
        options.set_preference('intl.accept_languages', user_language)
        browser = webdriver.Firefox(options=options)

    else:
        raise pytest.UsageError('--browser_name should be chrome or firefox')

    browser.implicitly_wait(5)
    yield browser
    print('\nQuit browser..')
    browser.quit()