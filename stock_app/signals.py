from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Sale, Purchase
from django.db import transaction

#django sinyallerini kullanarak sale ve purchase stok güncellemelein yapıldığı yer

@receiver(post_save, sender=Sale) #17 product un stock miktarını azaltır
def decrease_stock(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product = instance.product
            product.stock -= instance.quantity
            if product.stock < 0:
                raise ValueError('Stok miktarı yetersiz.')
            product.save()

@receiver(post_save, sender=Purchase)  # /önceki miktar ile yeni miktar arasındaki farkı hesaplar/ 21.satın alma işleminde stok miktarın arttırılması 
def update_stock_on_purchase(sender, instance, created, **kwargs):
    with transaction.atomic():
        product = instance.product
        if created:
            product.stock += instance.quantity
        else:
            # Güncelleme durumunda, önceki miktarı ve yeni miktarı karşılaştır
            original_quantity = instance.get_original_quantity()
            quantity_difference = instance.quantity - original_quantity
            product.stock += quantity_difference
        if product.stock < 0:
            raise ValueError('Stok miktarı yetersiz.')
        product.save()

@receiver(post_delete, sender=Purchase) # purchase silindiğinde stok mikt azalır 24
def update_stock_on_purchase_delete(sender, instance, **kwargs):
    with transaction.atomic():
        product = instance.product
        product.stock -= instance.quantity
        if product.stock < 0:
            raise ValueError('Stok miktarı negatif olamaz.')
        product.save()


@receiver(pre_save, sender=Purchase)
def remember_original_quantity(sender, instance, **kwargs): # mevcut ve önceki miktarlar arasında karşılastırma yapmak için 
    # Güncellenmeden önceki miktarı kaydet
    if instance.pk:
        original = Purchase.objects.get(pk=instance.pk)
        instance._original_quantity = original.quantity
    else:
        instance._original_quantity = 0
