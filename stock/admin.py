from django.contrib import admin
from .models import Account, StockBatch, StockItem, Patient, DispensationPayment, Dosage, Prescription

# Register your models here.
admin.site.register(Account)
admin.site.register(StockBatch)
admin.site.register(StockItem)
admin.site.register(Patient)
admin.site.register(DispensationPayment)
admin.site.register(Dosage)
admin.site.register(Prescription)
