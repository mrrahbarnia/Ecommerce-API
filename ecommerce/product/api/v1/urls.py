"""
URL's for the product app.
"""
from rest_framework.routers import DefaultRouter

from . import views

app_name = "product-api"

router = DefaultRouter()
router.register("category", views.CategoryViewSet)
router.register("product", views.ProductViewSet)


urlpatterns = []
urlpatterns += router.urls
