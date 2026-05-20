import re
import allure
from playwright.sync_api import expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.postal_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.error_message_container = self.page.locator("[data-test='error']")
        self.cancel_button = self.page.locator("#cancel")

    @allure.step("Заполнить поле First Name значением: '{first_name}'")
    def fill_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)

    @allure.step("Заполнить поле Last Name значением: '{last_name}'")
    def fill_last_name(self, last_name: str):
        self.last_name_input.fill(last_name)

    @allure.step("Заполнить поле Postal Code значением: '{postal_code}'")
    def fill_postal_code(self, postal_code: str):
        self.postal_code_input.fill(postal_code)

    @allure.step("Нажать кнопку 'Continue' (успешный переход)")
    def click_continue(self):
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)

    @allure.step("Нажать кнопку 'Continue' (ожидание ошибки)")
    def click_continue_with_error(self):
        self.continue_button.click()

    @allure.step("Проверить отображение ошибки: '{expected_text}'")
    def verify_error_message(self, expected_text: str):
        expect(self.error_message_container).to_have_text(expected_text)

    @allure.step("Нажать кнопку 'Cancel' на шаге чекаута")
    def click_cancel(self):
        self.cancel_button.click()
        from pages.cart_page import CartPage
        return CartPage(self.page)


class CheckoutOverviewPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.finish_button = self.page.locator("#finish")
        self.item_total_label = self.page.locator(".summary_subtotal_label")
        self.tax_label = self.page.locator(".summary_tax_label")
        self.total_label = self.page.locator(".summary_total_label")
        self.cart_items = self.page.locator(".cart_item")
        self.item_prices = self.page.locator(".inventory_item_price")

    def click_finish(self):
        self.finish_button.click()
        return CheckoutCompletePage(self.page)

    def get_item_total(self) -> float:
        text = self.item_total_label.text_content()
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        text = self.tax_label.text_content()
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.total_label.text_content()
        return float(text.split("$")[1])

    def get_calculated_items_sum(self) -> float:
        prices_text = self.item_prices.all_text_contents()
        return sum(float(price.replace("$", "")) for price in prices_text)

    @allure.step("Проверить математический расчет итоговой суммы (Item Total + Tax = Total)")
    def verify_total_calculation(self):
        item_total = self.get_item_total()
        tax = self.get_tax()
        total = self.get_total()
        assert abs(total - (item_total + tax)) < 0.01

    @allure.step("Проверить, что все цены округлены до 2 знаков после запятой (.XX)")
    def verify_prices_format(self):
        price_pattern = re.compile(r"\$\d+\.\d{2}$")

        item_total_text = self.item_total_label.text_content().strip()
        tax_text = self.tax_label.text_content().strip()
        total_text = self.total_label.text_content().strip()

        assert price_pattern.search(item_total_text)
        assert price_pattern.search(tax_text)
        assert price_pattern.search(total_text)

    @allure.step("Проверить корректность чекаута для нескольких товаров (ожидается: {expected_count})")
    def verify_multiple_items_checkout(self, expected_count: int):
        expect(self.cart_items).to_have_count(expected_count)

        calculated_sum = self.get_calculated_items_sum()
        displayed_item_total = self.get_item_total()
        assert abs(calculated_sum - displayed_item_total) < 0.01

        self.verify_total_calculation()


class CheckoutCompletePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.complete_header = self.page.locator(".complete-header")

    @allure.step("Проверить отображение сообщения об успешном заказе")
    def verify_checkout_complete_message(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")
