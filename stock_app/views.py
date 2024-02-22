from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from .models import Brand, Category, Firm, Product, Purchase, Sale
from .serializers import BrandSerializer, CategorySerializer, FirmSerializer, ProductSerializer, PurchaseSerializer, SaleSerializer




# CategoryViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name'] 
    filter_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# BrandViewSet
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# FirmViewSet
class FirmViewSet(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ProductViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['category', 'brand']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# PurchaseViewSet
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['firm__name']
    filterset_fields = ['firm', 'product']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# SaleViewSet
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['brand__name']
    filterset_fields = ['brand', 'product']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   
    def perform_create(self, serializer):  #22 satın alma işlemi oldğnda otomatik satın alan kullanıcıların bilgilerini kaydeder
        product = serializer.validated_data['product']    # satışı yapılacak ürünü alır
        quantity = serializer.validated_data['quantity']   #satılan ürün miktarı ..

        if quantity > product.stock:     # satılan mik >  stok mikt                 24
            raise ValidationError('Stokta yeterli ürün bulunmamaktadır.')

        product.stock -= quantity         #  stok 0 ın altına düşerse
        if product.stock < 0:
            raise ValidationError('Stok miktarı yetersiz.')
        product.save()

        serializer.save(user=self.request.user)   # satışı gerçeklestiren kullanıcıyı satış kaydına ekler 





  

