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
        return render(request, 'dr/dr_prescription_prescriptions.html')