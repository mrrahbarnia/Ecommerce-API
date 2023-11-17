"""
Init file for pytest package.
"""
import pytest
from pytest_factoryboy import register

from rest_framework.test import APIClient

from .factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory
)

register(BrandFactory)
register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)


@pytest.fixture
def client():
    """Sample client for http methods."""
    return APIClient()
