"""
Admin site for models.
"""
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe

from core.models.product import (
    Brand,
    Category,
    Product,
    ProductLine,
    ProductImage
)


class EditLinkInline(object):
    """Adding edit inline button for
    ProductLine instances for adding images."""
    def edit(self, instance):
        url = reverse(
            f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change', # noqa
            args=[instance.pk]
        )
        if instance.pk:
            """If there was any instances."""
            link = mark_safe("<a href='{u}'>edit</a>".format(u=url))
            return link
        else:
            return ""


class ProductImageInline(admin.TabularInline):
    """To adding ProductImage's instances to a
    ProductLine instance while creating it in admin site."""
    model = ProductImage


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    """Exhibiting ProductLine's instances in admin site."""
    inlines = [ProductImageInline]


class ProductLineInline(EditLinkInline, admin.TabularInline):
    """To adding ProductLine's instances to a
    Product instance while creating it in admin site."""
    model = ProductLine
    readonly_fields = ('edit',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Exhibiting Product's instances in admin site."""
    inlines = [ProductLineInline]


admin.site.register(Brand)
admin.site.register(Category)
