"""
Serializers for product app.
"""
from rest_framework import serializers

from core.models.product import (
    Product,
    Category,
    Brand
)


class CategorySerializer(serializers.ModelSerializer):
    """Converting data to json format for the category model."""

    class Meta:
        model = Category
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    """Converting data to json format for the brand model."""

    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Converting data to json format for the product model."""
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'
