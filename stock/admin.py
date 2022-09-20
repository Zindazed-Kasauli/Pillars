from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StockBatch)
admin.site.register(StockItem)
admin.site.register(DispensationPayment)
admin.site.register(Dosage)
admin.site.register(Prescription)