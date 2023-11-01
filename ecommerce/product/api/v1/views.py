"""
Views for product's API.
"""
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer
)
from core.models.product import (
    Category,
    Brand,
    Product
)


class CategoryViewSet(viewsets.ViewSet):
    """Returning a list of all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """Returning a list of all brands."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """Returning a list of all products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
