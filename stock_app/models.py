from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError


# Kategori Modeli
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Marka Modeli
class Brand(models.Model):
    name = models.CharField(max_length=255)
    image = models.TextField()

    def __str__(self):
        return self.name

# Ürün Modeli
class Product(models.Model):
    name = models.CharField(max_length=255)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) 
    stock = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)  # Otomatik oluşturulma zamanı
    updated = models.DateTimeField(auto_now=True)  # Otomatik güncellenme zamanı

   # auto_now_add=True parametresi, nesne ilk oluşturulduğunda geçerli zamanın otomatik olarak kaydedilmesini sağlar. 
   # auto_now=True, her nesne güncellendiğinde geçerli zamanın otomatik olarak kaydedilmesini sağlar.

    def __str__(self):
        return self.name 
    
# Firma Modeli
class Firm(models.Model):
    name = models.CharField(max_length=255) 
    phone = models.CharField(max_length=20)  
    address = models.TextField() 
    image = models.TextField()  
    created = models.DateTimeField(default=timezone.now)  # Varsayılan değer olarak şimdiki zamanı kullanır (hata verip durdu burda bu şekilde düzeldi)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

# Satın Alma Modeli
class Purchase(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE) 
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1) 
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    __original_quantity = None     #başlangıçtaki miktarı saklamak için

    def __init__(self, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)
        self.__original_quantity = self.quantity

    def get_original_quantity(self):
        return self.__original_quantity
   

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.quantity}"


    def save(self, *args, **kwargs):
        # price_total hesaplaması
        if not self.price or not self.quantity:
            raise ValidationError("Fiyat ve miktar bilgileri eksiksiz olmalıdır.")
        self.price_total = self.price * self.quantity
        super(Purchase, self).save(*args, **kwargs) 


# Satış Modeli
class Sale(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Kullanıcı modeli ile ilişki
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product modeli ile ilişki
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # Brand modeli ile ilişki
    quantity = models.SmallIntegerField()  # Satılan ürün miktarı
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Birim fiyat
    price_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Toplam fiyat
    created = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

  


    __original_quantity = None     #başlangıçtaki miktarı saklamak için [7-17-21-24]

    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)
        self.__original_quantity = self.quantity

    def get_original_quantity(self):
        return self.__original_quantity
   

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.quantity}"


    def save(self, *args, **kwargs):
        # price_total hesaplaması
        if not self.price or not self.quantity:
            raise ValidationError("Fiyat ve miktar bilgileri eksiksiz olmalıdır.")
        self.price_total = self.price * self.quantity
        super(Sale, self).save(*args, **kwargs) 
    
  

 