"""
Test models.
"""
import pytest

from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestBrandModel:
    """Tests for the Brand model."""

    def test_brand_output_str(self, brand_factory):
        """Test the __str__ method for the Brand model."""
        obj = brand_factory()

        assert str(obj) == obj.name


class TestCategoryModel:
    """Tests for the Category model."""

    def test_category_output_str(self, category_factory):
        """Test the __str__ method for the Category model."""
        obj = category_factory()

        assert str(obj) == obj.name


class TestProductModel:
    """Tests for the Product model."""

    def test_product_output_str(self, product_factory):
        """Test the __str__ method for the Product model."""
        obj = product_factory()

        assert str(obj) == obj.name


class TestProductLineModel:
    """Test for the ProductLine model."""

    def test_product_line_output_str(
            self, attribute_value_factory, product_line_factory
            ):
        """Test the __str__ method for the ProductLine model."""
        attribute_value_obj = attribute_value_factory()
        product_line_obj = product_line_factory.create(
            attribute_value=(attribute_value_obj, )
            )

        assert str(product_line_obj) == product_line_obj.sku

    def test_duplicate_order_values(
            self, product_line_factory, product_factory
            ):
        """Test preventing from inserting duplicate value for order field."""
        product_obj = product_factory()
        product_line_factory(order=1, product=product_obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product_obj)


class TestProductImageModel:
    """Test for the ProductImage model."""

    def test_product_image_output_str(self, product_image_factory):
        """Test the __str__ method for the ProductImage model."""
        obj = product_image_factory()

        assert str(obj) == obj.name

    def test_duplicate_order_values(
            self, product_line_factory, product_image_factory
    ):
        """Test preventing from inserting duplicate value for order field."""
        obj = product_line_factory()
        product_image_factory(product_line=obj, order=1)
        with pytest.raises(ValidationError):
            product_image_factory(product_line=obj, order=1)


class TestAttributeModel:
    """Test for the Attribute model."""

    def test_attribute_output_str(self, attribute_factory):
        """Test the __str__ method for the Attribute model."""
        obj = attribute_factory()

        assert str(obj) == obj.name


class TestAttributeValueModel:
    """Test for the AttributeValue model."""

    def test_attribute_value_output_str(self, attribute_value_factory):
        """Test the __str__ method for the Attribute model."""
        obj = attribute_value_factory()

        assert str(obj) == f"{obj.attribute}: {obj.value}"


class TestProductTypeModel:
    """Test for the ProductType model."""

    def test_product_type_output_str(
            self, attribute_factory, product_type_factory
            ):
        """Test the __str__ method for the ProductType model."""
        attribute_obj = attribute_factory()
        product_type_obj = product_type_factory.create(
            attribute=(attribute_obj,)
            )

        assert str(product_type_obj) == product_type_obj.name
