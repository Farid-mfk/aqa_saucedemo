import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def browser_instance():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=True, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture(autouse=True)
def page(browser_instance):
    """Стандартная страница для обычных тестов."""
    page = browser_instance.new_page()
    page.set_default_timeout(5_000)
    page.goto(URL_BASE)
    yield page


@pytest.fixture
def login_user_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_btn_login()
    yield page


@pytest.fixture
def slow_3g_context(browser_instance):
    """Фикстура для создания контекста браузера со скоростью Slow 3G (Без конфликтов asyncio)."""
    context = browser_instance.new_context()
    page = context.new_page()
    page.set_default_timeout(5_000)

    client = context.new_cdp_session(page)
    client.send("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 400,  # Задержка 400мс
        "downloadThroughput": 400000,  # ~400 Kbps
        "uploadThroughput": 150000  # ~150 Kbps
    })
    yield page
