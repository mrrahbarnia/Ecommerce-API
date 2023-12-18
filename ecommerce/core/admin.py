"""
Admin site for models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models.product import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductType,
)
from core.models.user import (
    Profile,
    ProfileImage
)

User = get_user_model()


class ProfileImageInline(admin.TabularInline):
    """To adding ProfileImage's instances to a
    Profile instance while creating it in admin site."""
    model = ProfileImage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Exhibiting Profile's instances in admin site."""
    inlines = [ProfileImageInline,]
    readonly_fields = ['user',]


@admin.register(User)
class UserAdmin(UserAdmin):
    """For customizing admin page."""
    ordering = ['id']
    model = User
    list_display = ("email", "is_verified", "is_staff")
    fieldsets = (
        (None, {'fields': ("email", "password")}),
        (_("Permissions"),
            {'fields':
             ("is_active", "is_verified",
              "is_staff", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ("last_login",)
    add_fieldsets = (
        (None, {
            "fields": (
                "email",
                "password1",
                "password2",
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
            )
        }),
    )


class EditLinkInline(object):
    """Adding edit inline button for
    ProductLine instances for adding images."""

    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",  # noqa
            args=[instance.pk],
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


class AttributeValueInline(admin.TabularInline):
    """To adding AttributeValues instances to a
    ProductLine instance while creating it in admin site."""

    model = AttributeValue.product_line_attribute_value.through


class AttributeValueProductInline(admin.TabularInline):
    """To adding AttributeValues instances to a
    ProductLine instance while creating it in admin site."""

    model = AttributeValue.product_attribute_value.through


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    """Exhibiting ProductLine's instances in admin site."""

    inlines = [ProductImageInline, AttributeValueInline]


class ProductLineInline(EditLinkInline, admin.TabularInline):
    """To adding ProductLine's instances to a
    Product instance while creating it in admin site."""

    model = ProductLine
    readonly_fields = ("edit",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Exhibiting Product's instances in admin site."""

    inlines = [ProductLineInline, AttributeValueProductInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """Exhibiting ProductType's instances in admin site."""
    inlines = [AttributeInline]


admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
