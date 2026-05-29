import time
import allure
import pytest

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD  # Ваши константы авторизации
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature("Performance and Reliability")
class TestPerformance:

    @allure.title("Время загрузки главной страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_perf_001_page_load_time(self, login_user_page):
        load_time_ms = login_user_page.evaluate(
            "() => window.performance.timing.loadEventEnd - window.performance.timing.navigationStart"
        )
        load_time_sec = load_time_ms / 1000
        allure.attach(f"{load_time_sec} сек", name="Фактическое время загрузки")

        assert load_time_sec < 3.0, f"Страница грузилась слишком долго: {load_time_sec} сек"

    @allure.title("Время отклика кнопки Login")
    @allure.severity(allure.severity_level.MINOR)
    def test_perf_002_login_button_response(self, page):
        page.goto(URL_BASE)
        login_page = LoginPage(page)

        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)

        start_time = time.time()
        login_page.click_btn_login()

        inventory_page = InventoryPage(page)
        inventory_page.verify_inventory_page_url()
        end_time = time.time()

        response_time = end_time - start_time
        allure.attach(f"{response_time} сек", name="Время отклика кнопки Login")

        assert response_time < 1.0, f"Кнопка Login откликнулась за {response_time} сек (ожидалось < 1 сек)"

    @pytest.mark.repeat(10)
    @allure.title("Стабильность при 10 последовательных прогонах")
    @allure.severity(allure.severity_level.NORMAL)
    def test_perf_003_stability_repeat(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Работа при медленном соединении (throttling Slow 3G)")
    @allure.severity(allure.severity_level.MINOR)
    def test_perf_004_slow_3g_network(self, slow_3g_context):
        page = slow_3g_context
        page.goto(URL_BASE)

        login_page = LoginPage(page)
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()

        inventory_page = InventoryPage(page)
        inventory_page.verify_inventory_page_url()
