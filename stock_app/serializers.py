from rest_framework import serializers
from .models import Product, Category, Brand, Purchase, Firm, Sale



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'brand', 'stock', 'created', 'updated']
        read_only_fields = ['stock'] #17 kullanıcılar tarafından apı üzerinden değiştirilememz


class BrandSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) 
    total_products = serializers.SerializerMethodField() #7 

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'total_products']
        # many=True, ilişkinin birden çok ürün içerebileceğini belirtir ve 
        # read_only=True, bu alanın sadece okunabilir olduğu anlamına gelir, yani API üzerinden bu alanla ilgili bir POST veya PUT isteği yapılamaz.
    def get_total_products(self, obj):
        # Category modeline bağlı ürünlerin sayısını döndürür.7.soru
        return obj.product_set.count()

class PurchaseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='product.category.name') 

    class Meta:
        model = Purchase
        fields = ['id', 'product', 'category_name', 'quantity', 'price', 'price_total', 'created', 'updated']
        read_only_fields = ['price_total']  

    def validate(self, data):   #18.soru
      
        if 'price' in data and 'quantity' in data:
            data['price_total'] = data['price'] * data['quantity']
        return data


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = '__all__' 

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'user', 'product', 'brand', 'quantity', 'price', 'price_total', 'created', 'updated']
        read_only_fields = ['price_total']

    def validate(self, data): #18
    
        if 'price' in data and 'quantity' in data:
            data['price_total'] = data['price'] * data['quantity']
        return data
