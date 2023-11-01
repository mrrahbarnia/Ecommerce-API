"""
Test API's endpoints for the product app.
"""
import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models.product import (
    Category,
    Brand,
    Product
)
from product.api.v1.serializers import (
    ProductSerializer,
    CategorySerializer,
    BrandSerializer
)


PRODUCT_LIST_URL = reverse('product-api:product-list')
BRAND_LIST_URL = reverse('product-api:brand-list')
CATEGORY_LIST_URL = reverse('product-api:category-list')


@pytest.fixture
def client():
    """Returning a client."""
    client = APIClient()
    return client


@pytest.mark.django_db
class TestEndPoints:
    """Test API's endpoints belong to product app."""

    def test_list_product_response_200(self, client):
        """Test listing products successfully with response 200."""
        sample_brand = Brand.objects.create(name='Test')
        Product.objects.create(name='Test1', brand_id=sample_brand.id)
        Product.objects.create(name='Test2', brand_id=sample_brand.id)

        res = client.get(PRODUCT_LIST_URL)
        serializer = ProductSerializer(res.data, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data
        assert len(res.data) == 2

    def test_list_brand_response_200(self, client):
        """Test listing brands successfully with response 200."""
        Brand.objects.create(name='Test1')
        Brand.objects.create(name='Test2')

        res = client.get(BRAND_LIST_URL)
        serializer = BrandSerializer(res.data, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data
        assert len(res.data) == 2

    def test_list_categories_response_200(self, client):
        """Test listing categories successfully with response 200."""
        Category.objects.create(name='Test1')
        Category.objects.create(name='Test2')

        res = client.get(CATEGORY_LIST_URL)
        serializer = CategorySerializer(res.data, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data
        assert len(res.data) == 2
