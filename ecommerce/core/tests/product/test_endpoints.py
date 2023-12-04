"""
Test API's endpoints for the product app.
"""
import pytest

from django.urls import reverse

from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    """Test Categories endpoints."""
    CATEGORY_LIST_URL = reverse('product-api:category-list')

    def test_get_category_list_response_200(self, category_factory, client):
        """Test get method for listing categories."""
        category_factory.create_batch(4, is_active=True)

        response = client.get(self.CATEGORY_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4


class TestProductEndpoints:
    """Test Products endpoints."""
    PRODUCT_LIST_URL = reverse('product-api:product-list')

    def test_get_product_list_response_200(self, product_factory, client):
        """Test get method for listing products."""
        product_factory.create_batch(4)

        response = client.get(self.PRODUCT_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_get_product_by_associated_slug(self, product_factory, client):
        """Test get products by a specific category."""
        product_factory(slug='Test-slug1')
        sample_product = product_factory(slug='Test-slug2')

        response = client.get(
            f'{self.PRODUCT_LIST_URL}{sample_product.slug}/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['slug'] == sample_product.slug

    def test_list_products_by_category_slug(
            self, category_factory, product_factory, client
            ):
        """Test returning products filtered by their categories slug."""
        sample_category1 = category_factory(slug='test-slug1')
        sample_category2 = category_factory(slug='test-slug2')
        product_factory(category=sample_category1)
        product_factory(category=sample_category2)

        response = client.get(
            f'{self.PRODUCT_LIST_URL}category/{sample_category1.slug}/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
