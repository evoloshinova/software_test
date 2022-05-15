import time

import pytest
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def wait(xpath, driver):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element

@pytest.fixture
def driver():
    driver = webdriver.Safari()
    driver.get("http://automationpractice.com/index.php")
    yield driver
    driver.close()

#если ввести валидный имейл, будет переход на страницу создания аккаунта
def test_registration(driver):
    signup = wait('//*[@id="header"]/div[2]/div/div/nav/div[1]/a', driver)
    signup.click()
    email_form = wait('//*[@id="email_create"]', driver)
    email_form.send_keys('adasd@aca.sdc')
    button = wait('//*[@id="SubmitCreate"]/span', driver).click()
    time.sleep(10)
    create = wait('// *[ @ id = "noSlide"] / h1', driver)
    assert create.text == 'Create an account'

#если ввести неправильный формат имейла, будет ошибка
def test_wrong_email(driver):
    signup = wait('//*[@id="header"]/div[2]/div/div/nav/div[1]/a', driver)
    signup.click()
    email_form = wait('//*[@id="email_create"]', driver)
    email_form.send_keys('adasd')
    button = wait('//*[@id="SubmitCreate"]/span', driver).click()
    error = wait('// *[ @ id = "create_account_error"] / ol / li', driver)
    assert error.text == 'Invalid email address.'

#проверяем, что если ввести незарегестрированного пользователя, аутентификации не будет
def test_wrong_login(driver):
    signup = wait('//*[@id="header"]/div[2]/div/div/nav/div[1]/a', driver)
    signup.click()
    email = wait('//*[@id="email"]', driver)
    email.send_keys("adawd@ada.ff")
    password = wait('//*[@id="passwd"]', driver)
    password.send_keys('adafsdg')
    button = wait('//*[@id="SubmitLogin"]/span', driver)
    button.click()
    error = wait('//*[@id="center_column"]/div[1]/p', driver)
    assert error.text == 'There is 1 error'

def test_menu_text(driver):
    women = wait('// *[ @ id = "block_top_menu"] / ul / li[1] / a', driver)
    dresses = wait('//*[@id="block_top_menu"]/ul/li[2]/a', driver)
    t_shirts = wait('//*[@id="block_top_menu"]/ul/li[3]/a', driver)
    assert women.text == "Women"
    assert dresses.text == "Dresses"
    assert t_shirts.text == "T-shirts"

#проверяем, что в корзину добавился один предмет
def test_add_1_to_cart(driver):
    women = wait('// *[ @ id = "block_top_menu"] / ul / li[1] / a', driver)
    women.click()
    add = wait('//*[@id="center_column"]/ul/li[1]/div/div[2]/div[2]/a[1]/span', driver)
    add.click()
    time.sleep(10)
    checkout = wait('//*[@id="layer_cart"]/div[1]/div[2]/div[4]/span', driver)
    checkout.click()
    time.sleep(10)
    cart = wait('//*[@id="header"]/div[3]/div/div/div[3]/div/a/b', driver)
    cart.click()
    summary = wait('//*[@id="summary_products_quantity"]', driver)
    time.sleep(10)
    assert summary.text == '1 Product'

def test_plus(driver):
    women = wait('// *[ @ id = "block_top_menu"] / ul / li[1] / a', driver)
    women.click()
    time.sleep(10)
    more = wait('//*[@id="center_column"]/ul/li[1]/div/div[2]/div[2]/a[2]/span', driver)
    more.click()
    plus = wait('//*[@id="quantity_wanted_p"]/a[2]/span/i', driver)
    plus.click()
    time.sleep(10)
    plus.click()
    time.sleep(10)
    cart = wait('//*[@id="header"]/div[3]/div/div/div[3]/div/a/b', driver)
    cart.click()
    time.sleep(20)
    summary = wait('//*[@id="summary_products_quantity"]', driver)
    assert summary.text == '3 Products'

def test_contact(driver):
    contact = wait('//*[@id="contact-link"]/a', driver)
    contact.click()
    time.sleep(20)
    assert driver.current_url == 'http://automationpractice.com/index.php?controller=contact'


if __name__ != '__main__':
    pass
else:
    test_registration(driver)
    test_wrong_email(driver)
    test_wrong_login(driver)
    test_menu_text(driver)
    test_add_1_to_cart(driver)
    test_plus(driver)
    test_contact(driver)




