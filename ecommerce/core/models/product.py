"""
Product app models.
"""
from django.db import models

from mptt.models import (
    TreeForeignKey,
    MPTTModel
)


class Category(MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True
    )

    class MPTTMeta:
        order_insertion_by = ['name']
        # verbose_plural_names = 'categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(
        Brand, related_name='brand', on_delete=models.CASCADE
    )
    category = TreeForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name