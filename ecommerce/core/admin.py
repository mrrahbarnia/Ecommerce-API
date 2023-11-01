"""
Admin site for models.
"""
from django.contrib import admin

from core.models.product import (
    Brand,
    Category,
    Product
)


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
