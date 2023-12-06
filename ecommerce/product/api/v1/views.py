"""
Views for product's API.
"""
from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCategorySerializer,
)
from core.models.product import Category, Product, ProductLine, ProductImage


class CategoryViewSet(viewsets.ViewSet):
    """Returning a list of all categories."""

    queryset = Category.objects.active()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """Returning a list of all products."""

    queryset = Product.objects.active()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def list(self, request):
        """Returning a list of all products."""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """Returning a product with the assigned slug."""
        serializer = self.serializer_class(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch(
                "product_line",
                queryset=ProductLine.objects.order_by('order')
            ))
            .prefetch_related(Prefetch(
                "product_line__product_image",
                queryset=ProductImage.objects.order_by('order')
            ))
            .prefetch_related(Prefetch(
                "product_line__attribute_value__attribute"
            ))
            .prefetch_related(Prefetch(
                "attribute_value__attribute"
            )),
            many=True,
        )
        return Response(serializer.data)

    @action(
            methods=["GET"],
            detail=False,
            url_path=r"category/(?P<cat_slug>[\w-]+)"
        )
    def list_product_by_category_slug(self, request, cat_slug=None):
        """Returning all products filtered by
        the associated category slug."""
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=cat_slug)
            .prefetch_related(
                Prefetch(
                    "product_line",
                    queryset=ProductLine.objects.order_by("order")
                )
            )
            .prefetch_related(
                Prefetch(
                    "product_line__product_image",
                    queryset=ProductImage.objects.filter(order=1),
                )
            ),
            many=True,
        )
        return Response(serializer.data)
