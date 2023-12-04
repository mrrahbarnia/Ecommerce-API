"""
Init file for pytest package.
"""
import pytest
from pytest_factoryboy import register

from rest_framework.test import APIClient

from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
    ProductTypeFactory,
    AttributeFactory,
    AttributeValueFactory,
    ProductAttributeValueFactory,
    ProductLineAttributeValueFactory
)

register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductAttributeValueFactory)
register(ProductLineAttributeValueFactory)


@pytest.fixture
def client():
    """Sample client for http methods."""
    return APIClient()
