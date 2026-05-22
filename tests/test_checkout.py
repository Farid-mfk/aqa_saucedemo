import allure
import pytest

from pages.inventory_page import InventoryPage
from playwright.sync_api import expect
from pages.checkout_page import CheckoutOverviewPage


@allure.feature("Checkout")
class TestCheckout:

    @allure.title("Полный успешный чекаут")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_checkout_form(first_name="Farid", last_name="Muborakshoev", postal_code="12345")
        checkout_page.click_continue()
        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_complete_page = checkout_overview_page.click_finish()
        checkout_complete_page.verify_checkout_complete_message()

    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error",
        [
            ("", "Muborakshoev", "12345", "Error: First Name is required"),
            ("Farid", "", "12345", "Error: Last Name is required"),
            ("Farid", "Muborakshoev", "", "Error: Postal Code is required"),
        ],
        ids=["Empty First Name", "Empty Last Name", "Empty Postal Code"]
    )
    @allure.title("Негативный чекаут: {ids}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_002_003_004(self, login_user_page, first_name, last_name, postal_code, expected_error):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()

        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()

        checkout_page.fill_checkout_form(
            first_name=first_name,
            last_name=last_name,
            postal_code=postal_code
        )

        checkout_page.click_continue()
        checkout_page.verify_error_message(expected_error)

    @allure.title("Валидация Postal code (формат)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_005(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_checkout_form(first_name="Farid", last_name="Muborakshoev", postal_code="12345")
        checkout_page.click_continue()
        checkout_overview_page = CheckoutOverviewPage(login_user_page)
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
        checkout_page.fill_checkout_form(first_name="Farid", last_name="Muborakshoev", postal_code="12345")
        checkout_page.click_continue()
        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_total_calculation()

    @allure.title("Округление копеек (граничный случай)")
    @allure.severity(allure.severity_level.MINOR)
    def test_checkout_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_checkout_form(first_name="Farid", last_name="Muborakshoev", postal_code="12345")
        checkout_page.click_continue()
        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_prices_format()

    @allure.title("Чекаут с несколькими товарами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_multiple_items_to_cart(count=3)
        cart_page = inventory_page.click_cart_icon()
        checkout_page = cart_page.click_checkout_button()
        checkout_page.fill_checkout_form(first_name="Farid", last_name="Muborakshoev", postal_code="12345")
        checkout_page.click_continue()
        checkout_overview_page = CheckoutOverviewPage(login_user_page)
        checkout_overview_page.verify_multiple_items_checkout(expected_count=3)
