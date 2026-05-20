import allure

from pages.inventory_page import InventoryPage
from playwright.sync_api import expect


@allure.feature("Checkout")
class TestCheckout:

    @allure.title("Полный успешный чекаут")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("12345")
        checkout_overview_page = checkout_page.click_continue()
        checkout_complete_page = checkout_overview_page.click_finish()
        checkout_complete_page.verify_checkout_complete_message()

    @allure.title("Чекаут с пустым First name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_002(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("12345")
        checkout_page.click_continue_with_error()
        checkout_page.verify_error_message("Error: First Name is required")

    @allure.title("Чекаут с пустым Last name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_003(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_first_name("Farid")
        checkout_page.fill_postal_code("12345")
        checkout_page.click_continue_with_error()
        checkout_page.verify_error_message("Error: Last Name is required")

    @allure.title("Чекаут с пустым Postal code")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_004(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.click_continue_with_error()
        checkout_page.verify_error_message("Error: Postal Code is required")

    @allure.title("Валидация Postal code (формат)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_005(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("ABCDE")
        checkout_overview_page = checkout_page.click_continue()
        expect(checkout_overview_page.finish_button).to_be_visible()

    @allure.title("Возврат к корзине из шага 1 чекаута")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_006(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        cart_page_returned = checkout_page.click_cancel()
        cart_page_returned.verify_cart_page_url()
        expect(cart_page_returned.cart_items).to_have_count(1)

    @allure.title("Возврат к покупкам из шага 1 чекаута")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_007(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        cart_page_returned = checkout_page.click_cancel()
        cart_page_returned.click_continue_shopping()
        inventory_page.verify_inventory_page_url()

    @allure.title("Расчёт итоговой суммы (математика)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_008(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("12345")
        checkout_overview_page = checkout_page.click_continue()
        checkout_overview_page.verify_total_calculation()

    @allure.title("Округление копеек (граничный случай)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()

        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()

        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("12345")

        checkout_overview_page = checkout_page.click_continue()

        # Проверяем, что на странице значения сумм округлены до формата .XX
        checkout_overview_page.verify_prices_format()

    @allure.title("Чекаут с несколькими товарами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        # Добавляем ровно 3 разных товара в корзину
        inventory_page.add_multiple_items_to_cart(count=3)

        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()

        checkout_page.fill_first_name("Farid")
        checkout_page.fill_last_name("Muborakshoev")
        checkout_page.fill_postal_code("12345")

        checkout_overview_page = checkout_page.click_continue()

        # Проверяем количество товаров, сходимость их цен и финальную сумму
        checkout_overview_page.verify_multiple_items_checkout(expected_count=3)
