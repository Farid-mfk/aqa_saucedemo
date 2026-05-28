import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.feature("Cross-browser and Cross-platform")
class TestCrossBrowser:

    @allure.title("Запуск сценария в разных браузерах (включая Headless/Headed)")
    @allure.link("TC_XB_001", name="Chromium")
    @allure.link("TC_XB_004", name="Headless vs Headed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_xb_001_to_004_browsers(self, login_user_page):
        """
        Этот сценарий валидирует кросс-браузерность (TC_XB_001-003)
        и идентичность поведения в режимах Headless/Headed (TC_XB_004).
        Браузеры определяются флагами командной строки.
        """
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.verify_cart_page_url()
        expect(cart_page.cart_items).to_have_count(1)

    @pytest.mark.parametrize(
        "width, height",
        [
            (1920, 1080),  # Монитор
            (1366, 768),  # Ноутбук
            (375, 667)  # Мобильный
        ],
        ids=["Desktop", "Laptop", "Mobile"]
    )
    @allure.title("Проверка адаптивности интерфейса: {ids}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_xb_005_resolutions(self, login_user_page, width, height):
        login_user_page.set_viewport_size({"width": width, "height": height})

        inventory_page = InventoryPage(login_user_page)
        expect(inventory_page.app_logo).to_be_visible()
        expect(inventory_page.burger_menu_button).to_be_enabled()
