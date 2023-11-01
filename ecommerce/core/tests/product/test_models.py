"""
Test models.
"""
import pytest

from ...models.product import (
    Product,
    Category,
    Brand
)


@pytest.mark.django_db
class TestModels:
    """Test creating an instance of a model successfully."""

    def test_create_category_instance_successfully(self):
        """Test creating an instance of the category model successfully."""
        sample_cat = Category.objects.create(name='Test')

        assert str(sample_cat) == sample_cat.name
        assert Category.objects.all().count() == 1

    def test_create_brand_instance_successfully(self):
        """Test creating an instance of the brand model successfully."""
        sample_brand = Brand.objects.create(name='Test')

        assert str(sample_brand) == sample_brand.name
        assert Brand.objects.all().count() == 1

    def test_create_product_instance_successfully(self):
        """Test creating an instance of the product model successfully."""
        sample_brand = Brand.objects.create(name='Test')
        sample_product = Product.objects.create(
            name='Test', brand_id=sample_brand.id
        )

        assert str(sample_product) == sample_product.name
        assert Product.objects.all().count() == 1
