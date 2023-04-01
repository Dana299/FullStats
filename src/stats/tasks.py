import random
from datetime import datetime, timedelta

from celery import shared_task

from .models import ProductHistory, ProductTracking
from .scraper import ProductPageParser


@shared_task(name='parse_and_save_product_history')
def parse_and_save_product_history(product_id, tracking_id):
    product_info = ProductPageParser().get_product_info(product_id)
    tracking = ProductTracking.objects.get(pk=tracking_id)
    ProductHistory.objects.create(
        product=tracking,
        name=product_info['product_name'],
        price=product_info['price'],
        discount_price=product_info['discount_price'],
        brand=product_info['brand_name'],
        supplier=product_info['supplier'],
    )
