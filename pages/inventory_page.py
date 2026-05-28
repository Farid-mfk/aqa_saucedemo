from playwright.sync_api import expect

from config.base import URL_BASE, URL_INV
from config.products import BACKPACK
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.logout_btn = self.page.locator("#logout_sidebar_link")
        self.burger_menu_btn = self.page.locator("#react-burger-menu-btn")
        self.cart_icon = self.page.locator(".shopping_cart_link")
        self.remove_button = self.page.locator("//button[text()='Remove']")
        self.add_to_cart_buttons = self.page.locator("//button[text()='Add to cart']")
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.title = self.page.locator(".title")
        self.backpack1 = self.page.get_by_text(BACKPACK)
        self.price = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//*[@class='inventory_item_price']")
        self.btn_add_to_card = self.page.locator(f"//*[text()='{BACKPACK}']/../../..//button")
        self.loc_price = "../../*[@class='inventory_item_price']"
        self.inventory_item = self.page.locator(".inventory_item")
        self.inventory_item_name = self.page.locator(".inventory_item_name")
        self.inventory_item_price = self.page.locator(".inventory_item_price")
        self.inventory_item_img = self.page.locator(".inventory_item_img")
        self.inventory_item_images = self.page.locator(".inventory_item_img img")
        self.sort_container = self.page.locator(".product_sort_container")
        self.inventory_item_button = self.page.locator(".inventory_item button")
        self.shopping_cart_badge = self.page.locator(".shopping_cart_badge")
        self.inventory_item_img_link = self.page.locator(".inventory_item_img a")
        self.inventory_details_name = self.page.locator(".inventory_details_name")
        self.remove_first_item = self.page.locator("button:has-text('Remove')")
        self.cart_button = self.page.locator("button:has-text('Add to cart')")
        self.app_logo = self.page.locator(".app_logo")
        self.burger_menu_button = self.page.locator("#react-burger-menu-btn")
        self.close_burger_menu_button = self.page.locator("#react-burger-cross-btn")
        self.all_items_link = self.page.locator("#inventory_sidebar_link")
        self.about_link = self.page.locator("#about_sidebar_link")
        self.logout_link = self.page.locator("#logout_sidebar_link")
        self.reset_link = self.page.locator("#reset_sidebar_link")

    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    def get_backpack1_price(self) -> str:
        price_ = self.price.text_content()
        return price_

    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    def have_title(self, title_text: str):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text(title_text)
        return True

    def get_inventory_items(self):
        return self.inventory_item.count()

    def get_inventory_item_names(self):
        return self.inventory_item_name.all_text_contents()

    def get_inventory_item_prices(self):
        return self.inventory_item_price.all_text_contents()

    def get_inventory_item_images(self):
        images = self.inventory_item_images.all()

        for img in images:
            is_displayed = img.evaluate("el => el.naturalWidth > 0")
            assert is_displayed

    def sort_items_by_price_low_to_high(self):
        self.sort_container.select_option(value="lohi")

    def get_inventory_item_prices_raw(self):
        price_strings = self.inventory_item_price.all_text_contents()
        return [float(p.replace('$', '')) for p in price_strings]

    def sort_items_by_price_high_to_low(self):
        self.sort_container.select_option(value="hilo")

    def sort_items_by_name_az(self):
        self.sort_container.select_option(value="az")

    def add_first_item_to_cart(self):
        self.inventory_item_button.first.click()

    def get_cart_badge_count(self):
        badge = self.shopping_cart_badge
        return badge.inner_text() if badge.is_visible() else "0"

    def click_first_item_image(self):
        self.inventory_item_img_link.first.click()

    def get_product_details_name(self):
        return self.inventory_details_name.inner_text()

    def remove_first_item_from_cart(self):
        self.remove_first_item.first.click()

    def add_to_cart_button(self):
        return self.cart_button.first.is_visible()

    def verify_items_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    def add_multiple_items_to_cart(self, count: int):
        add_buttons = self.add_to_cart_buttons
        for i in range(count):
            add_buttons.nth(i).click()

    def verify_first_item_button_is_remove(self):
        expect(self.remove_button).to_have_text("Remove")

    def verify_bucket_is_empty(self):
        expect(self.cart_badge).to_be_hidden()

    def click_cart_icon(self) -> CartPage:
        self.cart_icon.click()
        return CartPage(self.page)

    def verify_inventory_page_url(self):
        expect(self.page).to_have_url(f"{URL_BASE + URL_INV}")

    def reload_page(self):
        self.page.reload()

    def logout(self):
        self.burger_menu_btn.click()
        self.logout_btn.click()
        return LoginPage(self.page)

    def click_app_logo(self):
        self.app_logo.click()

    def open_burger_menu(self):
        self.burger_menu_button.click()

    def close_burger_menu(self):
        self.close_burger_menu_button.click()

    def check_menu_items_visible(self):
        expect(self.all_items_link).to_be_visible()
        expect(self.about_link).to_be_visible()
        expect(self.logout_link).to_be_visible()
        expect(self.reset_link).to_be_visible()
