"""
Product app models.
"""
import uuid
import os

from django.db import models
from django.core.exceptions import ValidationError

from mptt.models import TreeForeignKey, MPTTModel

from core.fields import OrderField

def product_image_file_path(instance, filename):
    """Generating a file path for a new profile image."""
    ext = os.path.splitext (filename)[1]
    unique_name = uuid.uuid4 ()
    filename = f'{unique_name}{ext}'

    path = os.path. join('uploads', 'product', filename)
    return path


class IsActiveQuerySet(models.QuerySet):
    """Returning all the instances with the
    attribute is_active set to true."""

    def active(self):
        queryset = self.filter(is_active=True)
        return queryset


class Category(MPTTModel):
    """This class defines all attributes of the Category model."""

    name = models.CharField(max_length=235, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )

    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """This class defines all attributes of the Product model."""

    name = models.CharField(max_length=230, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    product_type = models.ForeignKey(
        "ProductType", related_name="product_type", on_delete=models.PROTECT
    )
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        related_name="product_attribute_value",
        through="ProductAttributeValue",
    )

    objects = IsActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """This class defines all attributes of the Attribute model."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """This class defines all attributes of the AttributeValue model."""

    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        "Attribute", related_name="attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.attribute}: {self.value}"


class ProductLineAttributeValue(models.Model):
    """Link table for many to many relation between
    the AttributeValue model and the ProductLine model."""

    product_line = models.ForeignKey(
        "ProductLine",
        related_name="product_attribute_value_pr",
        on_delete=models.CASCADE,
    )
    attribute_value = models.ForeignKey(
        "AttributeValue",
        related_name="product_attribute_value_av",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("product_line", "attribute_value")

    def clean(self):
        queryset = (
            ProductLineAttributeValue.objects.filter(
                product_line=self.product_line
            )
            .filter(attribute_value=self.attribute_value)
            .exists()
        )

        if not queryset:
            attributes = Attribute.objects.filter(
                attribute__product_line_attribute_value=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(attributes):
                raise ValidationError("Duplicate attribute exists")

    def save(self, *args, **kwargs):
        self.full_clean
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_line.product.name}"


class ProductType(models.Model):
    """This class defines all attributes of the ProductType model."""

    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )
    attribute = models.ManyToManyField(
        "Attribute",
        related_name="product_type_attribute",
        through="ProductTypeAttribute",
    )

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    """This class defines all attributes of the ProductLine model."""

    price = models.DecimalField(max_digits=5, decimal_places=2)
    sku = models.CharField(max_length=10, unique=True)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, related_name="product_line", on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    weight = models.FloatField()
    product_type = models.ForeignKey(
        "ProductType",
        related_name="product_line_type",
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )

    objects = IsActiveQuerySet.as_manager()

    def clean(self, exclude=None):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProductLine.objects.filter(product=self.product)

        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        """Save method for running clean method."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.sku


class ProductImage(models.Model):
    """This class defines all attributes of the Image model."""

    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(
        upload_to=product_image_file_path, default="test.jpg"
    )
    product_line = models.ForeignKey(
        ProductLine, related_name="product_image", on_delete=models.CASCADE
    )
    order = OrderField(unique_for_field="product_line", blank=True)

    def clean(self, exclude=None):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProductImage.objects.filter(product_line=self.product_line)

        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        """Save method for running clean method."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_line.sku}_img"


class ProductTypeAttribute(models.Model):
    """Link table for many to many relation between
    the ProductType model and the Attribute model."""

    product_type = models.ForeignKey(
        ProductType,
        related_name="product_type_attribute_pt",
        on_delete=models.CASCADE
    )
    attribute = models.ForeignKey(
        Attribute,
        related_name="product_type_attribute_at",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("product_type", "attribute")

    def __str__(self):
        return f"{self.product_type}"


class ProductAttributeValue(models.Model):
    """Link table for many to many relation between
    the Product model and the AttributeValue model."""

    product = models.ForeignKey(
        Product,
        related_name="product_product_attribute_value",
        on_delete=models.CASCADE,
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        related_name="attribute_value_product_attribute_value",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("product", "attribute_value")

    def clean(self):
        queryset = (
            ProductAttributeValue.objects.filter(product=self.product)
            .filter(attribute_value=self.attribute_value)
            .exists()
        )

        if not queryset:
            attributes = Attribute.objects.filter(
                attribute__product_attribute_value=self.product
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(attributes):
                raise ValidationError("Duplicate attribute exists")

    def save(self, *args, **kwargs):
        self.full_clean
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product}"
