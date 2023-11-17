"""
Generating and mocking data for tests.
"""
import factory
from faker import Faker

from core.models.product import (
    Category,
    Brand,
    Product,
    ProductLine,
    ProductImage
)


class BrandFactory(factory.django.DjangoModelFactory):
    """Generating data for the Brand model tests."""

    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: '%s' % (Faker().name()))
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    """Generating data for the Category model tests."""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: '%s' % (Faker().name()))
    slug = name
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    """Generating data for the Product model tests."""

    class Meta:
        model = Product

    name = 'Green shoe'
    slug = 'Green-shoe'
    description = Faker().paragraph(nb_sentences=1)
    is_digital = Faker().pybool()
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    """Generating data for the ProductLine model tests."""

    class Meta:
        model = ProductLine

    price = 10.00
    sku = str(Faker().pyint())
    stock_qty = Faker().pyint()
    product = factory.SubFactory(ProductFactory)
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Generating data for the ProductImage model tests."""

    class Meta:
        model = ProductImage
    name = 'Sample name'
    alternative_text = Faker().paragraph(nb_sentences=1)
    url = Faker().url()
    product_line = factory.SubFactory(ProductLineFactory)
