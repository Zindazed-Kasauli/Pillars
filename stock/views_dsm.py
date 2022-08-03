from django.shortcuts import render, redirect

def drug_store_manager(request):
    return render(request, 'dsm/dsm_stock_add_stock_item.html')