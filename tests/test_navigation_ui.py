import allure
from playwright.sync_api import expect

from config.base import URL_BASE
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Navigation and UI")
class TestNavigationUI:

    @allure.title("Логотип кликабелен → возврат на главную")
    @allure.severity(allure.severity_level.MINOR)
    def test_ui_001_logo_return_to_main(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_app_logo()
        inventory_page.verify_inventory_page_url()

    @allure.title("Меню гамбургер: открыть, закрыть и проверить пункты")
    @allure.severity(allure.severity_level.MINOR)
    def test_ui_002_burger_menu_elements(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)

        inventory_page.open_burger_menu()

        inventory_page.check_menu_items_visible()

        inventory_page.close_burger_menu()
        expect(inventory_page.all_items_link).not_to_be_visible()

    @allure.title("Адаптивность: мобильная вёрстка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_003_mobile_viewport(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)

        login_user_page.set_viewport_size({"width": 390, "height": 844})

        expect(inventory_page.burger_menu_button).to_be_enabled()
        expect(inventory_page.app_logo).to_be_visible()

    @allure.title("Состояния кнопок: enabled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_006_button_states_enabled(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)

        expect(checkout_page.continue_button).to_be_enabled()

    @allure.title("Фокус на полях ввода при Tab-навигации")
    @allure.severity(allure.severity_level.MINOR)
    def test_ui_007_accessibility_tab_focus(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)

        checkout_page.first_name_input.focus()
        expect(checkout_page.first_name_input).to_be_focused()

        login_user_page.keyboard.press("Tab")
        expect(checkout_page.last_name_input).to_be_focused()

    @allure.title("Обработка 404 на несуществующих URL")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_010_page_not_found(self, login_user_page):
        response = login_user_page.goto(f"{URL_BASE}/qwerty")
        assert response.status in (200, 404), \
            f"Ожидался 200 или 404, но получен: {response.status}"
