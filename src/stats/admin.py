from django.contrib import admin

from .models import ProductHistory, ProductTracking


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'get_product_id',
        'name',
        'price',
        'discount_price',
        'brand',
        'supplier',
        'last_updated',
        'get_user',
    )

    def get_user(self, obj):
        return obj.product.user

    def get_product_id(self, obj):
        return obj.product.product_id

    get_user.short_description = 'user'
    get_product_id.short_description = 'product id'


@admin.register(ProductTracking)
class ProductTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product_id',
        'tracking_interval',
        'start_tracking_date',
        'end_tracking_date',
    )
