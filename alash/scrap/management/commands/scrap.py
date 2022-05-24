import random

from django.core.management.base import BaseCommand

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrap.models import TempTable


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.gets_data()

    def gets_data(self):
        for _ in range(3):
            try:
                # Заходит на стр. каспи клиент
                url = 'https://kaspi.kz/merchantcabinet/login?logout=true'

                options = Options()
                options.headless = False
                options.add_argument("--window-size=1920,1080")

                driver = webdriver.Chrome(
                    executable_path=(r"/home/alash/Downloads/dj-selenium-master/chromedriver/chromedriver"),
                    options=options)
                driver.get(url)
                driver.set_page_load_timeout(60)
                driver.implicitly_wait(20)

                # Установливает окно браузера в полный экран(потому что мешает подсказка-помощник сайта)
                driver.maximize_window()
                # Вбиваем логин и пароль

                mail = driver.find_element(By.ID, 'email')
                mail.send_keys('almas8891@gmail.com')

                password = driver.find_element(By.ID, 'password')
                password.send_keys('ANRI2022@rs')

                enter_btn = driver.find_element(By.XPATH, '//button[@class="button"]')
                driver.implicitly_wait(10)
                enter_btn.click()
                self.run_page(driver)

            except TimeoutException:
                driver.quit()
                continue
            except Exception as ex:
                driver.quit()
                continue
            else:
                driver.close()
                break
        # return render(request, 'scrap/main.html')

    def run_page(self, driver):
        for _ in range(3):
            try:
                delay = random.randint(4, 8)
                products_btn = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Товары")))
                driver.execute_script("arguments[0].click();", products_btn)
            except:
                driver.refresh()
                continue
            else:
                break

        # Цикл работает пока кнопка 'след' доступна
        while True:
            # for j in range(1):

            # Ждем пока стр загрузится
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='offer-managment__product-cell-link']")))
            # Название магазов
            count_shops = driver.find_elements_by_xpath("//a[@class='offer-managment__product-cell-link']")

            # # Цикл для записи данных товаров
            for i in range(len(count_shops)):
                # for i in range(10):
                self.gets_dt_good(driver, i)

            # Берем значение кнопки след 'true' или 'false'
            click_next = driver.find_element_by_xpath('//img[contains(@aria-label, "Next page")]'). \
                get_attribute('aria-disabled')
            click_next1 = driver.find_element_by_xpath('//img[contains(@aria-label, "Next page")]')

            # Если значение false то кликаем на кнопку след
            if click_next == 'false':  # Проверяет активна ли кнопка
                driver.execute_script('arguments[0].click();', click_next1)
            # Если нет то выходим из цикла(значит мы дошли до конца списка товаров)
            else:
                break

    def gets_dt_good(self, driver, i):
        try:
            vendor_code_goods = driver.find_elements_by_xpath('//div[@title="Артикул в системе продавца"]')[i].text

        except:
            vendor_code_goods = "Нет артикула товара"

        try:
            name_goods = driver.find_elements_by_xpath('//div[@title="Название в системе продавца"]')[i].text
        except:
            name_goods = "Нет название товара"

        print(name_goods)

        try:
            TempTable.objects.create(
                vend_code=vendor_code_goods,
                model=name_goods)
            print('added')

        except:
            print('already exists')