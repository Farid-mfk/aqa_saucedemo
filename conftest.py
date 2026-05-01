import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def page():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(3_000)
        page.goto(URL_BASE)
        yield page
        browser.close()


@pytest.fixture
def login_user_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_btn_login()
    yield page
