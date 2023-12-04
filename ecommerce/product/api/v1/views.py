"""
Views for product's API.
"""
from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    CategorySerializer,
    ProductSerializer
)
from core.models.product import (
    Category,
    Product
)


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
    lookup_field = 'slug'

    def list(self, request):
        """Returning a list of all products."""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """Returning a product with the assigned slug."""
        serializer = self.serializer_class(
            self.queryset.filter(slug=slug)
            .select_related('category')
            .prefetch_related(
                Prefetch('product_line__product_image'))
            .prefetch_related(
                Prefetch('product_line__attribute_value__attribute')
            ), many=True)
        return Response(serializer.data)

    @action(
            methods=['GET'],
            detail=False,
            url_path=r'category/(?P<cat_slug>[\w-]+)'
        )
    def list_product_by_category_slug(self, request, cat_slug=None):
        """Returning all products filtered by
        the associated category slug."""
        serializer = self.serializer_class(
            self.queryset.filter(category__slug=cat_slug), many=True
        )
        return Response(serializer.data)
