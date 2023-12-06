"""
Serializers for product app.
"""
from rest_framework import serializers

from core.models.product import (
    Product,
    Category,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
)


class CategorySerializer(serializers.ModelSerializer):
    """Converting data to json format for the Category model."""

    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    """Converting data to json format for the ProductImage model."""

    class Meta:
        model = ProductImage
        fields = (
            "order",
            "url",
            "alternative_text",
        )


class AttributeSerializer(serializers.ModelSerializer):
    """Converting data to json format for the Attribute model."""

    class Meta:
        model = Attribute
        fields = ("id", "name")


class AttributeValueSerializer(serializers.ModelSerializer):
    """Converting data to json format for the AttributeValue model."""

    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ("attribute", "value")


class ProductLineSerializer(serializers.ModelSerializer):
    """Converting data to json format for the ProductLine model."""

    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "order",
            "price",
            "sku",
            "stock_qty",
            "product_image",
            "attribute_value",
        )

    def to_representation(self, instance):
        """For representing more understandable data."""
        data = super().to_representation(instance)
        attr_values = {}

        av_data = data.pop("attribute_value")
        for _ in av_data:
            attr_values.update({_["attribute"]["name"]: _["value"]})

        data.update({"specifications": attr_values})
        return data


class ProductSerializer(serializers.ModelSerializer):
    """Converting data to json format for the Product model."""

    product_line = ProductLineSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "pid",
            "slug",
            "description",
            "product_line",
            "attribute_value",
        ]

    def to_representation(self, instance):
        """For representing more understandable data."""
        data = super().to_representation(instance)
        attr_values = {}

        av_data = data.pop("attribute_value")
        for _ in av_data:
            attr_values.update({_["attribute"]["name"]: _["value"]})

        data.update({"attributes": attr_values})
        return data


class ProductLineCategorySerializer(serializers.ModelSerializer):
    """Serializing data for the endpoint
    that shows products by category slug."""

    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["price", "product_image"]


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializing data for the endpoint
    that shows products by category slug."""

    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "pid", "created_at", "product_line"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_line = data.pop("product_line")
        if product_line:
            price = product_line[0]["price"]
            img = product_line[0]["product_image"]
            data.update({"price": price})
            data.update({"image": img})
        return data
