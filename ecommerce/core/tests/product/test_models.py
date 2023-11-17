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
        sample_brand = brand_factory()

        assert str(sample_brand) == sample_brand.name


class TestCategoryModel:
    """Tests for the Category model."""

    def test_category_output_str(self, category_factory):
        """Test the __str__ method for the Category model."""
        sample_category = category_factory()

        assert str(sample_category) == sample_category.name


class TestProductModel:
    """Tests for the Product model."""

    def test_product_output_str(self, product_factory):
        """Test the __str__ method for the Product model."""
        sample_product = product_factory()

        assert str(sample_product) == sample_product.name


class TestProductLineModel:
    """Test for the ProductLine model."""

    def test_product_line_output_str(self, product_line_factory):
        """Test the __str__ method for the ProductLine model."""
        sample_productline = product_line_factory()

        assert str(sample_productline) == sample_productline.sku

    def test_duplicate_order_values(
            self, product_line_factory, product_factory
            ):
        """Test preventing from inserting duplicate value for order field."""
        sample_product = product_factory()
        product_line_factory(order=1, product=sample_product)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=sample_product)


class TestProductImageModel:
    """Test for the ProductImage model."""

    def test_product_image_output_str(self, product_image_factory):
        """Test the __str__ method for the ProductImage model."""
        sample_productimage = product_image_factory()

        assert str(sample_productimage) == sample_productimage.name

    def test_duplicate_order_values(
            self, product_line_factory, product_image_factory
    ):
        """Test preventing from inserting duplicate value for order field."""
        sample_productline = product_line_factory()
        product_image_factory(product_line=sample_productline, order=1)
        with pytest.raises(ValidationError):
            product_image_factory(product_line=sample_productline, order=1)
