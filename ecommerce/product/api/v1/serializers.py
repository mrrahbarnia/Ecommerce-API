"""
Serializers for product app.
"""
from rest_framework import serializers

from core.models.product import (
    Product,
    Category,
    Brand,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue
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


class AttributeSerializer(serializers.ModelSerializer):
    """Converting data to json format for the Attribute model."""

    class Meta:
        model = Attribute
        fields = ('id', 'name')


class AttributeValueSerializer(serializers.ModelSerializer):
    """Converting data to json format for the AttributeValue model."""
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ('attribute', 'value')


class ProductLineSerializer(serializers.ModelSerializer):
    """Converting data to json format for the ProductLine model."""
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'order',
            'price',
            'sku',
            'stock_qty',
            'product_image',
            'attribute_value',
        )

    def to_representation(self, instance):
        """For representing more understandable data."""
        data = super().to_representation(instance)
        prod_img = []
        attr_values = {}

        images = data.pop('product_image')
        for _ in images:
            prod_img.append(_['order'])

        av_data = data.pop('attribute_value')
        for _ in av_data:
            attr_values.update({_['attribute']['id']: _['value']})

        data.update({'product_image': prod_img})
        data.update({'specifications': attr_values})
        return data


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
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'brand_name',
            'category_name', 'attributes', 'product_line'
            ]

    def get_attributes(self, obj):
        attributes = Attribute.objects.filter(
            product_type_attribute__product_product_type=obj.id
            )
        return AttributeSerializer(attributes, many=True).data

    def to_representation(self, instance):

        data = super().to_representation(instance)
        type_specifications = {}

        attributes = data.pop('attributes')
        for _ in attributes:
            type_specifications.update({_['id']: _['name']})
        data.update({'type specifications': type_specifications})
        return data
