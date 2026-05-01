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
