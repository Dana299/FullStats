import re
from typing import TypedDict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProductInfo(TypedDict):
    brand_name: str
    product_name: str
    price: int
    discount_price: int
    supplier: str


class ProductPageParser:

    WEBDRIVER_PATH = "/usr/local/bin/chromedriver"
    PRODUCT_URL_PATTERN = "https://www.wildberries.ru/catalog/%s/detail.aspx"

    def get_product_info(self, product_id: str) -> ProductInfo:
        try:
            source_html = self._get_source_html(product_id)
            soup = BeautifulSoup(source_html, features="lxml")

            product_info: ProductInfo = {
                'brand_name': self._get_product_brandname(soup),
                'product_name': self._get_product_name(soup),
                'price': self._get_product_price(soup),
                'discount_price': self._get_product_discount_price(soup),
                'supplier': self._get_product_supplier(soup),
            }

            return product_info

        except Exception as e:
            print(e)
            raise ValueError(f"Failed to retrieve source html for product {product_id}: {str(e)}")

    def _get_source_html(self, product_id: str) -> str:

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-dev-shm-usage')

        with webdriver.Chrome(options=chrome_options) as wd:
            wd.maximize_window()
            wd.get(url=ProductPageParser.PRODUCT_URL_PATTERN % product_id)
            # wait for the seller info button to be clickable
            supplier_info_button = WebDriverWait(wd, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'seller-info__tip-info'))
            )
            # scroll to the seller info button and click on it
            actions = ActionChains(wd)
            actions.move_to_element(supplier_info_button)
            actions.click()
            actions.perform()
            # wait until modal window with supplier pops out
            WebDriverWait(wd, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tooltip-supplier'))
            )
            # load html code
            source_html = wd.execute_script("return document.body.innerHTML;")

            return source_html

    def _get_product_brandname(self, soup: BeautifulSoup) -> str:
        product_page_header = soup.find(class_="product-page__header")
        brand_name = product_page_header.find(
            attrs={"data-link": re.compile(r'.*brandName.*')}
        )
        return brand_name.text

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        product_page_header = soup.find(class_="product-page__header")
        product_name = product_page_header.find(
            attrs={"data-link": re.compile(r'.*goodsName.*')}
        )
        return product_name.text

    def _get_price_from_str(self, str_: str) -> int:
        """
        Removes non-breaking space and ruble sign
        and converts from rubles to pennies.
        """
        price_in_pennies = int(str_.replace('\xa0', '').replace('₽', '')) * 100
        return price_in_pennies

    def _get_product_price(self, soup: BeautifulSoup) -> int:
        discount_price_str = soup.find(class_="price-block__old-price")
        return self._get_price_from_str(discount_price_str.text)

    def _get_product_discount_price(self, soup: BeautifulSoup) -> int:
        price = soup.find(class_="price-block__final-price")
        return self._get_price_from_str(price.text)

    def _get_product_supplier(self, soup: BeautifulSoup) -> str:
        supplier = soup.find(class_="tooltip-supplier") \
                       .find(class_="tooltip__content") \
                       .find("p")
        return supplier.text
