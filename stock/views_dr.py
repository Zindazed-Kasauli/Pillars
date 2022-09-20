from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Q
from datetime import datetime

#doctor search stock view
def dr_stock(request, action):
    if action == "search_stock_item" or action == "stock":
        items = StockItem.objects.all().order_by('name')
        if request.method == "GET":
            search = request.GET.get("search","")
            items = StockItem.objects.filter(name__icontains = search).order_by('name')
        return render(request, 'dr/dr_stock_search_stock_item.html',{'items':items})

#doctor prescriptions
def dr_prescription(request, action):
    if action == "prescriptions":
        if request.method == "GET":
            search = request.GET.get("search","")
            batch = Prescription.objects.filter(patient__icontains = search).order_by("-date")
        else:
            batch = Prescription.objects.order_by("-date")        
        return render(request, 'dr/dr_prescription_prescriptions.html',{'batch':batch})

def dr_prescription_details(request, action, id):
    if action == "bill_prescription" or action == "prescription":
        bill = Prescription.objects.get(Q(id = id))
        batch = StockBatch.objects.filter(Q(prescription = bill) & Q(invoice_number = "Prescription"))
                
        return render(request, 'dr/dr_prescription_prescription_view.html',{
            "bill":bill,
            "batch":batch,
        })