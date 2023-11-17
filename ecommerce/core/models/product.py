"""
Product app models.
"""
from django.db import models
from django.core.exceptions import ValidationError

from mptt.models import (
    TreeForeignKey,
    MPTTModel
)

from core.fields import OrderField


class IsActiveQuerySet(models.QuerySet):
    """Returning all the instances with the
    attribute is_active set to true."""
    def active(self):
        queryset = self.filter(is_active=True)
        return queryset


class Category(MPTTModel):
    """This class defines all attributes of the Category model."""
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True
    )

    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """This class defines all attributes of the Brand model."""
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    objects = IsActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    """This class defines all attributes of the Product model."""
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(
        Brand, related_name='brand', on_delete=models.CASCADE
    )
    category = TreeForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

    objects = IsActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    """This class defines all attributes of the ProductLine model."""
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sku = models.CharField(max_length=150)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, related_name='product_line', on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field='product', blank=True)

    objects = IsActiveQuerySet.as_manager()

    def clean(self, exclude=None):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProductLine.objects.filter(product=self.product)

        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        """Save method for running clean method."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.sku


class ProductImage(models.Model):
    """This class defines all attributes of the Image model."""
    name = models.CharField(max_length=250)
    alternative_text = models.CharField(max_length=250)
    url = models.ImageField(upload_to=None, default='test.jpg')
    product_line = models.ForeignKey(
        ProductLine, related_name='product_image', on_delete=models.CASCADE
    )
    order = OrderField(unique_for_field='product_line', blank=True)

    def clean(self, exclude=None):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProductImage.objects.filter(product_line=self.product_line)

        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        """Save method for running clean method."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
