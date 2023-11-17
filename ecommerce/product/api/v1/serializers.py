"""
Serializers for product app.
"""
from rest_framework import serializers

from core.models.product import (
    Product,
    Category,
    Brand,
    ProductLine,
    ProductImage
)


class CategorySerializer(serializers.ModelSerializer):
    """Converting data to json format for the Category model."""

    class Meta:
        model = Category
        fields = ['name']


class ProductImageSerializer(serializers.ModelSerializer):
    """Converting data to json format for the ProductImage model."""

    class Meta:
        model = ProductImage
        fields = (
            'order', 'name', 'url', 'alternative_text',
        )


class ProductLineSerializer(serializers.ModelSerializer):
    """Converting data to json format for the ProductLine model."""
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'order',
            'price',
            'sku',
            'stock_qty',
            'product_image'
        )


class BrandSerializer(serializers.ModelSerializer):
    """Converting data to json format for the Brand model."""

    class Meta:
        model = Brand
        exclude = ['id', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    """Converting data to json format for the Product model."""
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(
        source='category.name', required=False
    )
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'brand_name',
            'category_name', 'product_line'
            ]
