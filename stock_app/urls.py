from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('brands', views.BrandViewSet)
router.register('products', views.ProductViewSet)
router.register('purchases', views.PurchaseViewSet)
router.register('sales', views.SaleViewSet)
router.register('firms', views.FirmViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



