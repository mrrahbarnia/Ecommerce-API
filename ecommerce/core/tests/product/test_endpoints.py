"""
Test API's endpoints for the product app.
"""
import pytest

from django.urls import reverse

from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    """Test Categories endpoints."""

    CATEGORY_LIST_URL = reverse("product-api:category-list")

    def test_get_category_list_response_200(self, category_factory, client):
        """Test get method for listing categories."""
        category_factory.create_batch(4, is_active=True)

        response = client.get(self.CATEGORY_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4


class TestProductEndpoints:
    """Test Products endpoints."""

    PRODUCT_LIST_URL = reverse("product-api:product-list")

    def test_get_product_list_response_200(self, product_factory, client):
        """Test get method for listing products."""
        product_factory.create_batch(4)

        response = client.get(self.PRODUCT_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_get_product_by_associated_slug(self, product_factory, client):
        """Test get products by a specific category."""
        product_factory(slug="Test-slug1")
        sample_product = product_factory(slug="Test-slug2")

        response = client.get(f"{self.PRODUCT_LIST_URL}{sample_product.slug}/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["slug"] == sample_product.slug

    def test_return_product_with_ordered_product_line_by_associated_slug(
            self, product_factory, product_line_factory, client
    ):
        """Test returning products with ordered product lines
        by their order field by the associated product's slug."""
        sample_product = product_factory()
        sample_prod_line1 = product_line_factory(
            product=sample_product, order=1
        )
        sample_prod_line2 = product_line_factory(
            product=sample_product, order=2
        )

        response = client.get(f"{self.PRODUCT_LIST_URL}{sample_product.slug}/")

        assert (
            response.data[0]['product_line'][0]['order']
        ) == sample_prod_line1.order
        assert (
            response.data[0]['product_line'][1]['order']
        ) == sample_prod_line2.order

    def test_return_product_with_ordered_product_image_by_associated_slug(
            self, product_factory, product_image_factory,
            product_line_factory, client
    ):
        """Test returning products with ordered product images
        by their order field by the associated product's slug."""
        sample_product = product_factory()
        sample_prod_line = product_line_factory(product=sample_product)
        sample_prod_img1 = product_image_factory(
            product_line=sample_prod_line, order=1
        )
        sample_prod_img2 = product_image_factory(
            product_line=sample_prod_line, order=2
        )

        response = client.get(f"{self.PRODUCT_LIST_URL}{sample_product.slug}/")

        assert len(response.data) == 1
        assert (
            response.data[0]['product_line'][0]['product_image'][0]['order']
        ) == sample_prod_img1.order
        assert (
            response.data[0]['product_line'][0]['product_image'][1]['order']
        ) == sample_prod_img2.order

    def test_list_products_by_category_slug(
        self, category_factory, product_factory, client
    ):
        """Test returning products filtered by their categories slug."""
        sample_category1 = category_factory(slug="test-slug1")
        sample_category2 = category_factory(slug="test-slug2")
        product_factory(category=sample_category1)
        product_factory(category=sample_category2)

        response = client.get(
            f"{self.PRODUCT_LIST_URL}category/{sample_category1.slug}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_return_first_product_line_first_product_image_by_category_slug(
        self,
        product_factory,
        product_line_factory,
        product_image_factory,
        category_factory,
        client,
    ):
        """Test returning only the first product line and the first
        product image that belongs to the first product line when
        returning products by their category slug."""
        sample_category = category_factory(slug="test-slug")
        sample_product = product_factory(category=sample_category)
        sample_prod_line1 = product_line_factory(
            product=sample_product, price=10, order=1
        )
        sample_prod_line2 = product_line_factory(
            product=sample_product, price=20, order=2
        )
        sample_prod_img1 = product_image_factory(
            product_line=sample_prod_line1, order=1
        )
        sample_prod_img2 = product_image_factory(
            product_line=sample_prod_line2, order=2
        )

        response = client.get(
            f"{self.PRODUCT_LIST_URL}category/{sample_category.slug}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["price"] == "10.00"
        assert response.data[0]["price"] != "20.00"
        assert len(response.data[0]["image"]) == 1
        assert response.data[0]["image"][0]["order"] == sample_prod_img1.order
        assert response.data[0]["image"][0]["order"] != sample_prod_img2.order
