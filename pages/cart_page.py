import allure
from playwright.sync_api import expect
from config.base import URL_BASE, URL_CART
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.continue_shopping_button = self.page.locator("#continue-shopping")
        self.cart_items = self.page.locator(".cart_item")
        self.checkout_button = self.page.locator("#checkout")

    @allure.step("Нажать кнопку 'Continue Shopping'")
    def click_continue_shopping(self):
        self.continue_shopping_button.click()

    @allure.step("Проверить URL страницы корзины")
    def verify_cart_page_url(self):
        expect(self.page).to_have_url(f"{URL_BASE + URL_CART}")

    @allure.step("Проверить, что корзина пуста")
    def verify_cart_is_empty(self):
        expect(self.cart_items).to_have_count(0)

    @allure.step("Нажать кнопку 'Checkout'")
    def click_checkout_button(self):
        self.checkout_button.click()
