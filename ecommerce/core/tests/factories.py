"""
Generating and mocking data for tests.
"""
import factory
from faker import Faker

from core.models.product import (
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
    ProductLineAttributeValue,
    ProductAttributeValue
)

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    """Generating data for the Category model tests."""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: '%s' % (fake.name()))
    slug = name


class ProductTypeFactory(factory.django.DjangoModelFactory):
    """Generating data for the ProductType model tests."""

    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: '%s' % (Faker().name()))

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        """Generating relations for the
        many to many field,it's not mandatory."""
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    """Generating data for the Product model tests."""

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: ('name_%s') % n)
    slug = factory.Sequence(lambda n: ('slug_%s' % n))
    pid = factory.Sequence(lambda n: '%s' % (fake.pyint()))
    description = fake.paragraph(nb_sentences=1)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        """Generating relations for the
        many to many field,it's not mandatory."""
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductLineFactory(factory.django.DjangoModelFactory):
    """Generating data for the ProductLine model tests."""

    class Meta:
        model = ProductLine

    price = 10.00
    sku = factory.Sequence(lambda n: '%s' % (fake.pyint()))
    stock_qty = Faker().pyint()
    product = factory.SubFactory(ProductFactory)
    weight = 10.00
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        """Generating relations for the
        many to many field,it's not mandatory."""
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Generating data for the ProductImage model tests."""

    class Meta:
        model = ProductImage
    alternative_text = Faker().paragraph(nb_sentences=1)
    url = Faker().url()
    product_line = factory.SubFactory(ProductLineFactory)


class AttributeFactory(factory.django.DjangoModelFactory):
    """Generating data for the Attribute model tests."""

    class Meta:
        model = Attribute
    name = factory.Sequence(lambda n: ('name_%s') % n)
    description = Faker().paragraph(nb_sentences=1)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    """Generating data for the AttributeValue model tests."""

    class Meta:
        model = AttributeValue
    value = Faker().name()
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineAttributeValueFactory(
    factory.django.DjangoModelFactory
):
    """Generating data for the
    ProductLineAttributeValue model tests."""

    class Meta:
        model = ProductLineAttributeValue

    product_line = factory.SubFactory(ProductLineFactory)
    attribute_value = factory.SubFactory(AttributeValueFactory)


class ProductAttributeValueFactory(
    factory.django.DjangoModelFactory
):
    """Generating data for the ProductAttributeValue model tests."""

    class Meta:
        model = ProductAttributeValue

    product = factory.SubFactory(ProductFactory)
    attribute_value = factory.SubFactory(AttributeValueFactory)
