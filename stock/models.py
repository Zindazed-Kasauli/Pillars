from unicodedata import name
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class StockItem(models.Model):
    name = models.CharField(max_length=200)
    strength = models.CharField(max_length=200)
    drug_type = models.CharField(max_length=200)
    cat1_price = models.IntegerField()
    account = models.ForeignKey(User, related_name="stockItem_accounts", on_delete=models.CASCADE) #account(dsm) enters stock item, also account(dispenser) requests for stock_item
    store_quantity = models.IntegerField(default=0)
    dispensary_quantity = models.IntegerField(default=0)
    # prescription = models.ForeignKey("Prescription", related_name="stockItem_prescriptions", on_delete=models.CASCADE)#stock_item receives Prescription
    # dispensationPayment = models.ForeignKey("DispensationPayment", related_name="stockItem_dispensation_payments", on_delete=models.CASCADE) #dispensation payment has stock_items
    
    def __str__(self):
        return f"{self.name} {self.drug_type} - {self.strength}"
        pass

class StockBatch(models.Model):
    invoice_number = models.CharField(max_length=300)
    quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    amount = models.FloatField()
    date = models.DateField()
    pharmacy = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    unit_pack = models.IntegerField()
    stock_item = models.ForeignKey("StockItem", related_name="stockBatch_stock_items", on_delete=models.CASCADE) #stock_batch has stock_item
    account = models.ForeignKey(User, related_name="stockBatch_accounts", on_delete=models.CASCADE) #account enters stock_item

    def __str__(self):
        return self.invoice_number
        pass

class Prescription(models.Model):
    bill = models.FloatField()
    account = models.ForeignKey(User, related_name="prescription_accounts", on_delete=models.CASCADE) #account/user enters prescription
    patient = models.ForeignKey("Patient", related_name="prescription_patients", on_delete=models.CASCADE) #patient has prescription
    # account = models.ForeignKey(User, related_name="prescription_accounts", on_delete=models.CASCADE) #account(dispenser) enter prescription

    def __str__(self):
        return self.bill
        pass

class Dosage(models.Model):
    dosage = models.CharField(max_length=200)
    stock_batch = models.ForeignKey("StockBatch", related_name="dosage_stock_batches", on_delete=models.CASCADE) #dosage is an attribute of the relationship, stockItem receives prescription
    prescription = models.ForeignKey("Prescription", related_name="dosage_prescriptions", on_delete=models.CASCADE) 

    def __str__(self):
        return self.dosage
        pass

class DispensationPayment(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    remarks = models.CharField(max_length=200)
    account = models.ForeignKey(User, related_name="dispensation_accounts", on_delete=models.CASCADE) #account(dispenser) dispenses dispensation_payment
    prescription = models.ForeignKey("Prescription", related_name="dispensation_prescriptions", on_delete=models.CASCADE) #prescription has dispensation_payments
    patient = models.ForeignKey("Patient", related_name="dispensation_patients", on_delete=models.CASCADE) #patient makes dispensation payment

    def __str__(self):
        return self.amount
        pass

class Patient(models.Model):
    name = models.CharField(max_length=200)
    account = models.ForeignKey(User, related_name="patients_accounts", on_delete=models.CASCADE) #account(dispenser) enters patient

    def __str__(self):
        return self.name
        pass