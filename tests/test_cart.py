import allure

from config.users import USER2_NAME, USERS_PASSWORD
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
class TestCart:

    @allure.title("Добавление одного товара")
    @allure.severity(allure.severity_level.MINOR)
    def test_cart_001(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Добавление нескольких разных товаров")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_002(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_multiple_items_to_cart(count=3)
        inventory_page.verify_items_in_bucket("3")

    @allure.title("Добавление одного товара несколько раз")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_003(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_first_item_button_is_remove()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Удаление товара из корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_004(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_items_in_bucket("1")
        inventory_page.remove_first_item_from_cart()
        inventory_page.verify_bucket_is_empty()

    @allure.title("Переход в корзину с любой страницы")
    @allure.severity(allure.severity_level.MINOR)
    def test_cart_006(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        cart_page = inventory_page.click_cart_icon()
        cart_page.verify_cart_page_url()

    @allure.title("Возврат к покупкам из корзины")
    @allure.severity(allure.severity_level.MINOR)
    def test_cart_007(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        cart_page = inventory_page.click_cart_icon()
        cart_page.click_continue_shopping()
        inventory_page.verify_inventory_page_url()

    @allure.title("Пустая корзина: отображение сообщения")
    @allure.severity(allure.severity_level.MINOR)
    def test_cart_008(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        cart_page = inventory_page.click_cart_icon()
        cart_page.verify_cart_is_empty()

    @allure.title("Сохранение корзины после перезагрузки страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_009(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_items_in_bucket("1")
        inventory_page.reload_page()
        inventory_page.verify_items_in_bucket("1")

    @allure.title("Изоляция корзины при смене пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_010(self, login_user_page):
        inventory_page = InventoryPage(login_user_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.verify_items_in_bucket("1")

        login_page = inventory_page.logout()
        login_page.fill_username(USER2_NAME)
        login_page.fill_password(USERS_PASSWORD)
        login_page.click_btn_login()
        inventory_page_user2 = InventoryPage(login_user_page)
        inventory_page_user2.verify_items_in_bucket("1")
