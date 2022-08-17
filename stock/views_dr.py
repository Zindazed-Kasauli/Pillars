from django.shortcuts import render, redirect

#doctor search stock view
def dr_stock(request, action):
    if action == "search_stock_item" or action == "stock":
        return render(request, 'dr/dr_stock_search_stock_item.html')

#doctor prescriptions
def dr_prescription(request, action):
    if action == "prescriptions":
        return render(request, 'dr/dr_prescription_prescriptions.html')