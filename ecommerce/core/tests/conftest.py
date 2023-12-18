"""
Init file for pytest package.
"""
import pytest
from pytest_factoryboy import register
from django.contrib.auth import get_user_model
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
    ProductLineAttributeValueFactory,
)

User = get_user_model()

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

@pytest.fixture
def create_user():
    """Create and return a new user."""
    user = User.objects.create_user(
        email='Test@example.com',
        password='Test123456'
    )
    return user

@pytest.fixture
def create_superuser():
    """Create and return a new admin user."""
    user = User.objects.create_superuser(
        email='Test@example.com',
        password='Test12345'
    )
    return user