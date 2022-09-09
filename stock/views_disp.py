from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Q
from datetime import datetime

#dispenser stock views
def disp_stock(request, action):
    if action == "request_stock" or action == "stock":
        return render(request, 'disp/disp_stock_request_stock.html')
    elif action == "search_stock":
        items = StockItem.objects.all().order_by('name')
        if request.method == "GET":
            search = request.GET.get("search","")
            items = StockItem.objects.filter(name__icontains = search).order_by('name')
        return render(request, 'disp/disp_stock_search_stock_item.html',{'items':items})
    elif action == "give_out_stock":
        if request.method == "POST":
            form = StockBatchForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    batch.save()
                    form.cleaned_data['stock_item'].dispensary_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} given out"
                else:
                    message = f"{batch['stock_item']} has already been given out"
                batchForm = StockBatchForm(initial={
                    'destination': batch['destination'],
                    'date':batch['date'],
                    'amount': 0,
                    'invoice_number': 'give_out',
                    'pharmacy': "Dispensary",
                    }) 
                return render(request, 'disp/disp_stock_give_out_stock.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])),
                    "message":message,
                    })
        batchForm = StockBatchForm(initial={
                    'amount': 0,
                    'invoice_number': 'give_out',
                    'pharmacy': "Dispensary",
                    })
        return render(request, 'disp/disp_stock_give_out_stock.html',{
            'batchForm':batchForm,
        })
    elif action == "adjustments_losses":
        if request.method == "GET":
            form = StockBatchForm(request.GET)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    batch.save()
                    form.cleaned_data['stock_item'].dispensary_quantity += form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} added"
                else:
                    message = f"{batch['stock_item']} has already been added"
                batchForm_a = StockBatchForm(initial={
                    'destination': 'Dispensary',
                    'date':batch['date'],
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    }) 
                batchForm_l = StockBatchForm(initial={
                    'pharmacy': "Dispensary",
                    'amount': 0,
                    'invoice_number': 'loss',
                    })
                return render(request, 'disp/disp_stock_adjustments_losses.html',{
                    "batchForm_a":batchForm_a,
                    "batchForm_l":batchForm_l,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])),
                    "message":message,
                    })
        if request.method == "POST":
            form = StockBatchForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    batch.save()
                    form.cleaned_data['stock_item'].dispensary_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} removed as loss"
                else:
                    message = f"{batch['stock_item']} has already been removed as loss"
                batchForm_l = StockBatchForm(initial={
                    'pharmacy': 'Dispensary',
                    'date':batch['date'],
                    'amount': 0,
                    'invoice_number': 'loss',
                    }) 
                batchForm_a = StockBatchForm(initial={
                    'destination': "Dispensary",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
                return render(request, 'disp/disp_stock_adjustments_losses.html',{
                    "batchForm_l":batchForm_l,
                    "batchForm_a":batchForm_a,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])),
                    "message":message,
                    })
        batchForm_a = StockBatchForm(initial={
                    'destination': "Dispensary",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
        batchForm_l = StockBatchForm(initial={
                    'pharmacy': "Dispensary",
                    'amount': 0,
                    'invoice_number': 'loss',
                    })
        return render(request, 'disp/disp_stock_adjustments_losses.html',{
            'batchForm_l':batchForm_l,
            'batchForm_a':batchForm_a,
        })
    elif action == "stock_price_list":
        return redirect('disp_stock','search_stock')
        return render(request, 'disp/disp_stock_stock_price_list.html')

#dispenser report views
def disp_reports(request, action):
    if action == "daily_report" or action == "reports":
        return render(request, 'disp/disp_report_daily_report.html')
    elif action == "notifications":
        return render(request, 'disp/disp_report_notifications.html')

#dispenser prescription views
def disp_prescription(request, action):
    if action == "bill_prescription" or action == "prescription":
        return render(request, 'disp/disp_prescription_bill_prescription.html')
    elif action == "prescriptions":
        return render(request, 'disp/disp_prescription_prescriptions.html')
    
def disp_delete(request, action, id):
    if action == "batchItem":
        batch_item = StockBatch.objects.get(id = id)
        invoice = batch_item.invoice_number
        if invoice == 'give_out' or invoice == 'loss':
            batch_item.stock_item.dispensary_quantity += batch_item.unit_pack * batch_item.quantity
        else:
            batch_item.stock_item.dispensary_quantity -= batch_item.unit_pack * batch_item.quantity
        batch_item.stock_item.save()
        StockBatch.objects.get(id = id).delete()
        
        if invoice == 'loss' or invoice == 'adjustment':
            batchForm_a = StockBatchForm(initial={
                    'destination': "Dispensary",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
            batchForm_l = StockBatchForm(initial={
                        'pharmacy': "Dispensary",
                        'amount': 0,
                        'invoice_number': 'loss',
                        })
            return render(request, 'disp/disp_stock_adjustments_losses.html',{
                'batchForm_l':batchForm_l,
                'batchForm_a':batchForm_a,
            })
        
        date = request.GET.get('date',False)
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
            date = date.date()
            
        if invoice == 'give_out':
            destination = request.GET.get('destination',False)
            if destination:
                batchForm = StockBatchForm(initial={
                'invoice_number': 'give_out',
                'amount': 0,
                'pharmacy':batch_item.pharmacy,
                'date':date
                }) 
                return render(request, 'disp/disp_stock_give_out_stock.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = 'give_out') & Q(pharmacy = batch_item.pharmacy)& Q(destination = destination)),
                    })
            else:
                batchForm = StockBatchForm()
                return render(request, 'disp/disp_stock_give_out_stock.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    })
        else:
            pharmacy = request.GET.get('pharmacy',False)
            invoice_number = request.GET.get('invoice_number',False)
            itemForm = StockItemForm()
            if pharmacy:
                batchForm = StockBatchForm(initial={
                'invoice_number': invoice_number,
                'pharmacy':pharmacy,
                'date':date
                }) 
                return render(request, 'disp/dsm_stock_add_stock_item.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = invoice_number) & Q(pharmacy = pharmacy)),
                    })
            else:
                batchForm = StockBatchForm()
                return render(request, 'disp/dsm_stock_add_stock_item.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    })