from config.products import PRODUCTS_NAMES, PRODUCTS_PRICES
from pages.inventory_page import InventoryPage

class TestInv:

    def test_inv_001(self, login_user_page):
        """ Отображение всех 6 товаров """
        inventory_page = InventoryPage(login_user_page)
        items = inventory_page.get_inventory_items()
        assert items == 6

    def test_inv_002(self, login_user_page):
        """ Проверка названий всех товаров """
        inventory_page = InventoryPage(login_user_page)
        items_name = inventory_page.get_inventory_item_names()
        assert items_name == PRODUCTS_NAMES

    def test_inv_003(self, login_user_page):
        """ Проверка цен всех товаров """
        inventory_page = InventoryPage(login_user_page)
        items_price = inventory_page.get_inventory_item_prices()
        assert items_price == PRODUCTS_PRICES

    def test_inv_004(self, login_user_page):
        """ Проверка изображений товаров """
        inventory_page = InventoryPage(login_user_page)
        inventory_page.get_inventory_item_images()

    def test_inv_005(self, login_user_page):
        """Сортировка по цене (низкая → высокая)"""
        inventory_page = InventoryPage(login_user_page)
        inventory_page.sort_items_by_price_low_to_high()
        actual_prices = inventory_page.get_inventory_item_prices_raw()
        expected_prices = sorted(actual_prices)
        assert actual_prices == expected_prices

    def test_inv_006(self, login_user_page):
        """Сортировка по цене (высокая → низкая)"""
        inventory_page = InventoryPage(login_user_page)
        inventory_page.sort_items_by_price_high_to_low()
        actual_prices = inventory_page.get_inventory_item_prices_raw()
        expected_prices = sorted(actual_prices, reverse=True)
        assert actual_prices == expected_prices

    def test_inv_007(self, login_user_page):
        """Сортировка по названию (A→Z)"""
        inventory_page = InventoryPage(login_user_page)
        inventory_page.sort_items_by_name_az()
        actual_names = inventory_page.get_inventory_item_names()
        expected_names = sorted(actual_names)
        assert actual_names == expected_names

    def test_inv_008(self, login_user_page):
        """Фильтрация после добавления в корзину"""
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_badge_count() == "1"
        inventory_page.sort_items_by_price_high_to_low()
        assert inventory_page.get_cart_badge_count() == "1"

    def test_inv_009(self, login_user_page):
        """Клик по изображению товара (если есть переход)"""
        inventory_page = InventoryPage(login_user_page)
        expected_name = inventory_page.get_inventory_item_names()[0]
        inventory_page.click_first_item_image()
        assert "inventory-item.html" in login_user_page.url
        actual_name = login_user_page.locator(".inventory_details_name").inner_text()
        assert actual_name == expected_name

    def test_inv_010(self, login_user_page):
        """Проверка кнопки "Remove" после добавления в корзину"""
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        remove_button = login_user_page.locator("button:has-text('Remove')").first
        assert remove_button.is_visible()
        assert inventory_page.get_cart_badge_count() == "1"
        remove_button.click()
        assert inventory_page.get_cart_badge_count() == "0"
        add_button = login_user_page.locator("button:has-text('Add to cart')").first
        assert add_button.is_visible()
