from django.conf import settings
from django.db import models


class ProductTracking(models.Model):
    """ Model for products tracked by users. """

    class TrackingIntervalChoices(models.Choices):
        ONE_HOUR = 1
        TWELVE_HOURS = 12
        ONE_DAY = 24

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()

    tracking_interval = models.IntegerField(
        choices=TrackingIntervalChoices.choices,
        default=TrackingIntervalChoices.TWELVE_HOURS,
    )
    start_tracking_date = models.DateTimeField()
    end_tracking_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"Tracking product {self.product_id} for user {self.user}"


class ProductHistory(models.Model):
    """ Model for product info. """

    product = models.ForeignKey(ProductTracking, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    brand = models.CharField(max_length=120)
    supplier = models.CharField(max_length=120)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Product {self.product.product_id}"
