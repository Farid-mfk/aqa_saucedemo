import allure
import pytest
from playwright.sync_api import expect

from config.users import FIRST_NAME, LAST_NAME, POSTAL_CODE, INVALID_POSTAL_CODE
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage


@allure.feature("Checkout")
class TestCheckout:

    @allure.title("Полный успешный чекаут")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=POSTAL_CODE)
        checkout_page.click_continue()

        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.click_finish()

        checkout_complete_page = CheckoutCompletePage(login_user_page)
        checkout_complete_page.verify_checkout_complete_message()

    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error",
        [
            ("", LAST_NAME, POSTAL_CODE, "Error: First Name is required"),
            (FIRST_NAME, "", POSTAL_CODE, "Error: Last Name is required"),
            (FIRST_NAME, LAST_NAME, "", "Error: Postal Code is required"),
        ],
        ids=["Empty First Name", "Empty Last Name", "Empty Postal Code"]
    )
    @allure.title("Негативный чекаут: {ids}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_002_003_004(self, login_user_page, first_name, last_name, postal_code, expected_error):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=first_name, last_name=last_name, postal_code=postal_code)
        checkout_page.click_continue()
        checkout_page.verify_error_message(expected_error)

    @allure.title("Валидация Postal code (формат)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_005(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=INVALID_POSTAL_CODE)
        checkout_page.click_continue()

        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        expect(checkout_overview_page.finish_button).to_be_visible()

    @allure.title("Возврат к корзине из шага 1 чекаута")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_006(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.click_cancel()

        cart_page_returned = CartPage(login_user_page)
        cart_page_returned.verify_cart_page_url()
        expect(cart_page_returned.cart_items).to_have_count(1)

    @allure.title("Возврат к покупкам из шага 1 чекаута")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_007(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.click_cancel()

        cart_page_returned = CartPage(login_user_page)
        cart_page_returned.click_continue_shopping()

        inventory_page.verify_inventory_page_url()

    @allure.title("Расчёт итоговой суммы (математика)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_008(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=POSTAL_CODE)
        checkout_page.click_continue()

        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_total_calculation()

    @allure.title("Округление копеек (граничный случай)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=POSTAL_CODE)
        checkout_page.click_continue()

        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_prices_format()

    @allure.title("Чекаут с несколькими товарами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_multiple_items_to_cart(count=3)
        inventory_page.click_cart_icon()

        cart_page = CartPage(login_user_page)
        cart_page.click_checkout_button()

        checkout_page = CheckoutPage(login_user_page)
        checkout_page.fill_checkout_form(first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=POSTAL_CODE)
        checkout_page.click_continue()

        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_multiple_items_checkout(expected_count=3)
