from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Q, Sum, F
from datetime import datetime

def myint(value):
    return round((value) - ((value)%-100))

#dispenser stock views
def disp_stock(request, action):
    if action == "request_stock" or action == "stock":
        if request.method == "POST":
            form = StockBatchForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy']) & Q(stock_item = batch['stock_item'])& Q(amount = 0)).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    batch.save()
                    # form.cleaned_data['stock_item'].dispensary_quantity += form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    # form.cleaned_data['stock_item'].save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} added to the request batch"
                else:
                    message = f"{batch['stock_item']} already exists in the request batch"
                batchForm = StockBatchForm(initial={
                    'invoice_number': 'requisition',
                    'amount': 0,
                    'pharmacy':'Drug Store',
                    'destination':'Dispensary',
                    'date':batch['date']
                    }) 
                return render(request, 'disp/disp_stock_request_stock.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])& Q(amount = 0)),
                    "message":message,
                    })
        batchForm = StockBatchForm(initial={
                    'invoice_number': 'requisition',
                    'amount': 0,
                    'pharmacy':'Drug Store',
                    'destination':'Dispensary',
                    })
        return render(request, 'disp/disp_stock_request_stock.html',{
            "batchForm":batchForm,
            "batch":StockBatch.objects.filter(Q(invoice_number = 'requisition') & Q(pharmacy = "Drug Store")& Q(destination = 'Dispensary')& Q(amount = 0)),

            })
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
                    form.cleaned_data['stock_item'].dispensary_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.dispensary_quantity = form.cleaned_data['stock_item'].dispensary_quantity                    
                    batch.save()
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
                    form.cleaned_data['stock_item'].dispensary_quantity += form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.dispensary_quantity = form.cleaned_data['stock_item'].dispensary_quantity
                    batch.save()
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
                    form.cleaned_data['stock_item'].dispensary_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.dispensary_quantity = form.cleaned_data['stock_item'].dispensary_quantity
                    batch.save()
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
        items = []
        for stock_item in StockItem.objects.all():
            if StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Drug Store')).order_by('-date').exists():
                item = dict()
                item['item'] = stock_item
                item['start'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Drug Store')).order_by('date').first().dispensary_quantity
                item['stop'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Drug Store')).order_by('-date').first().dispensary_quantity
                try:
                    item['quantity_received'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date()) & Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Drug Store') | Q(invoice_number = 'give_out')| Q(invoice_number = 'loss')| Q(invoice_number = 'bill')| Q(invoice_number = 'Prescription')| Q(invoice_number = 'payment')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                except AttributeError:
                    item['quantity_received'] = 0
                try:
                    item['quantity_taken'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date()) & Q(date__gte = datetime.today().date()) &( Q(invoice_number = 'give_out')| Q(invoice_number = 'loss')| Q(invoice_number = 'bill')| Q(invoice_number = 'Prescription')| Q(invoice_number = 'payment'))).exclude(Q(pharmacy = 'Drug Store')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                except AttributeError:
                    item['quantity_taken'] = 0
                items.append(item)
        return render(request, 'disp/disp_report_daily_report.html',{'items':items})
    elif action == "notifications":
        green = StockItem.objects.filter(Q(dispensary_quantity__lte = 100) & Q(dispensary_quantity__gt = 40))
        yellow = StockItem.objects.filter(Q(dispensary_quantity__lte = 40) & Q(dispensary_quantity__gt = 5))
        red = StockItem.objects.filter(Q(dispensary_quantity__lte = 5))
        return render(request, 'disp/disp_report_notifications.html',{
            'green':green,
            'yellow':yellow,
            'red':red,
        })

#dispenser prescription views
def disp_prescription_details(request, action, id):
    if action == "bill_prescription" or action == "prescription":
        bill = Prescription.objects.get(Q(id = id))
        if request.method == 'POST' and bill.balance > 0:
            date = request.POST['date']
            amount_paid = int(request.POST['amount_paid'])
            remarks = request.POST['remarks']
            
            payment = DispensationPayment(
                date = date,
                amount = amount_paid,
                remarks = remarks,
                account = request.user,
                prescription = bill
            )
            payment.save()
            
            bill.balance -= amount_paid
            bill.save()
            
            sub_amount = amount_paid + bill.stashed_amount
            max_freq = 0
            min_unit_cost = 999999
            min_price = 999999
            for item in bill.prescription_stock_batch.filter(invoice_number = 'bill').order_by('dosages__unit_cost','dosages__quantity'):
                if max_freq < item.dosages.frequency:
                    max_freq = item.dosages.frequency
                if min_unit_cost > item.dosages.unit_cost:
                    min_unit_cost = item.dosages.unit_cost
                if item.dosages.quantity:
                    if min_price > item.dosages.unit_cost/item.dosages.quantity:
                        min_price = item.dosages.unit_cost/item.dosages.quantity
                print("Zindazed, the problem is here. Do you see this Zindazed")
                if item.dosages.quantity <= 0 and item.quantity > 0:
                    print("Zindazed, the problem is here. Do you see this Zindazed 1.1")
                    for quantity in reversed(range(item.quantity)):
                        print("Zindazed, the problem is here. Do you see this Zindazed 1.2")
                        if sub_amount >= (item.amount/item.quantity*(quantity+1)):
                            print("Zindazed, the problem is here. Do you see this Zindazed 1.3")
                            sub_amount -= (item.amount/item.quantity*(quantity+1))
                            item_payment = StockBatch(
                                invoice_number = 'payment',
                                quantity = quantity+1,
                                amount = (item.amount/item.quantity*(quantity+1)),
                                date = date,
                                dispensary_quantity = item.stock_item.dispensary_quantity - quantity+1,
                                pharmacy = 'Dispensary',
                                destination = item.destination,
                                unit_pack = 1,
                                stock_item = item.stock_item,
                                account = request.user,
                                prescription = bill,
                                dosages = item.dosages,
                            )
                            item_payment.save()
                            item_payment.dispensation_payment.add(payment),
                            item.amount -= (item.amount/item.quantity*(quantity+1))
                            item.quantity -= quantity+1
                            item.save()
                            item.stock_item.dispensary_quantity -= quantity+1
                            item.stock_item.save()
                            break
                elif item.quantity >= item.dosages.quantity:
                    print("Zindazed, the problem is here. Do you see this Zindazed 2.1")
                    if sub_amount >= item.dosages.unit_cost:
                        print("Zindazed, the problem is here. Do you see this Zindazed 2.2")
                        sub_amount -= item.dosages.unit_cost
                        item_payment = StockBatch(
                            invoice_number = 'payment',
                            quantity = item.dosages.quantity,
                            amount = item.dosages.unit_cost,
                            date = date,
                            pharmacy = item.pharmacy,
                            destination = item.destination,
                            unit_pack = item.unit_pack,
                            stock_item = item.stock_item,
                            account = request.user,
                            dispensary_quantity = item.stock_item.dispensary_quantity - item.dosages.quantity,
                            prescription = bill,
                            dosages = item.dosages,
                        )
                        item_payment.save()
                        item_payment.dispensation_payment.add(payment),
                        item.quantity -= item.dosages.quantity
                        item.amount -= item.dosages.unit_cost
                        item.save()
                        item.stock_item.dispensary_quantity -= item.dosages.quantity
                        item.stock_item.save()
            
            is_there = True
            print("Zindazed, the problem is here. Do you see this Zindazed 3.1")
            while sub_amount >= min_unit_cost and is_there:
                is_there = False
                print("Zindazed, the problem is here. Do you see this Zindazed 3.2")
                for freq in reversed(range(max_freq)):
                    print("Zindazed, the problem is here. Do you see this Zindazed 3.3")
                    for item in bill.prescription_stock_batch.filter(invoice_number = 'bill').order_by('-dosages__frequency','dosages__unit_cost'):
                        print("Zindazed, the problem is here. Do you see this Zindazed 3.4")
                        if item.dosages.quantity > 0 and item.quantity >= item.dosages.quantity:
                            print("Zindazed, the problem is here. Do you see this Zindazed 3.5")
                            if item.dosages.frequency > freq and freq > 0 and sub_amount >= item.dosages.unit_cost:
                                print("Zindazed, the problem is here. Do you see this Zindazed 3.6")
                                sub_amount -= item.dosages.unit_cost
                                item_payment = StockBatch.objects.get(Q(invoice_number = 'payment') & Q(dispensation_payment = payment) & Q(stock_item = item.stock_item))
                                item_payment.quantity += item.dosages.quantity
                                item_payment.amount += item.dosages.unit_cost
                                item_payment.save()
                                item.quantity -= item.dosages.quantity
                                item.amount -= item.dosages.unit_cost
                                item.save()
                                item.stock_item.dispensary_quantity -= item.dosages.quantity
                                item.stock_item.save()
                                is_there = True
            
            print("Zindazed, the problem is here. Do you see this Zindazed 4.1")
            is_there = True
            while sub_amount >= min_price and is_there:
                print("Zindazed, the problem is here. Do you see this Zindazed 4.2")
                is_there = False
                for item in bill.prescription_stock_batch.filter(invoice_number = 'bill').order_by('stock_item__cat1_price'):
                    print("Zindazed, the problem is here. Do you see this Zindazed 4.3")
                    if item.dosages.quantity > 0 and item.quantity >= 1:
                        print("Zindazed, the problem is here. Do you see this Zindazed 4.4")
                        if sub_amount >= item.dosages.unit_cost/item.dosages.quantity:
                            print("Zindazed, the problem is here. Do you see this Zindazed 4.5")
                            sub_amount -= item.dosages.unit_cost/item.dosages.quantity
                            if StockBatch.objects.filter(Q(invoice_number = 'payment') & Q(dispensation_payment = payment) & Q(stock_item = item.stock_item)).exists():
                                item_payment = StockBatch.objects.get(Q(invoice_number = 'payment') & Q(dispensation_payment = payment) & Q(stock_item = item.stock_item))
                                item_payment.quantity += 1
                                item_payment.amount += item.dosages.unit_cost/item.dosages.quantity
                                item_payment.save()
                            else:
                                item_payment = StockBatch(
                                    invoice_number = 'payment',
                                    quantity = 1,
                                    amount = item.dosages.unit_cost/item.dosages.quantity,
                                    date = date,
                                    pharmacy = item.pharmacy,
                                    destination = item.destination,
                                    unit_pack = item.unit_pack,
                                    stock_item = item.stock_item,
                                    account = request.user,
                                    dispensary_quantity = item.stock_item.dispensary_quantity - 1,
                                    prescription = bill,
                                    dosages = item.dosages,
                                )
                                item_payment.save()
                            item.amount -= item.dosages.unit_cost/item.dosages.quantity
                            item.quantity -= 1
                            item.save()
                            item.stock_item.dispensary_quantity -= 1
                            item.stock_item.save()
                            is_there = True
                         
            print("Zindazed, the problem is here. Do you see this Zindazed 5")
            bill.stashed_amount = sub_amount
            bill.save()    
            return render(request, 'disp/disp_prescription_prescriptions_view.html',{
            "batch":StockBatch.objects.filter(Q(invoice_number = 'payment') & Q(dispensation_payment = payment)),
            "bill":bill,
        })                  
        return render(request, 'disp/disp_prescription_prescriptions_view.html',{
            "bill":bill,
        })
    
def disp_prescription(request, action):
    if action == "bill_prescription" or action == "prescription":
        if request.method == "POST":
            quantity = int(request.POST['quantity_per_time'])
            frequency = int(request.POST['frequency'])
            details = request.POST['details']
            form = StockBatchForm(request.POST)
            category = int(request.POST['category'])
            if form.is_valid():
                batch = form.cleaned_data
                amount = 0
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])& Q(date = batch['date'])).exists():
                    batch2 = form.save(commit=False)
                    batch2.account = request.user
                    if category == 3:
                        amount = round(batch2.quantity * batch2.stock_item.cat1_price * 3)
                        unit_cost = round(quantity * batch2.stock_item.cat1_price * 3)
                    elif category == 2:
                        amount = round(batch2.quantity * batch2.stock_item.cat1_price * 1.5)
                        unit_cost = round(quantity * batch2.stock_item.cat1_price * 1.5)
                    elif category == 1:
                        amount = round(batch2.quantity * batch2.stock_item.cat1_price)
                        unit_cost = round(quantity * batch2.stock_item.cat1_price)
                    batch2.amount = amount
                    batch2.save()
                    
                    if StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(date = batch['date'])).first().prescription:
                        batch2.prescription = StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(date = batch['date'])).first().prescription
                        batch2.prescription.bill += amount
                        batch2.prescription.balance += amount
                        batch2.prescription.save()
                        batch2.save()
                        dose = Dosage(
                            quantity = quantity,
                            frequency = frequency,
                            details = details,
                            unit_cost = unit_cost,
                            prescription = batch2.prescription,
                        )
                        dose.save()
                        batch2.dosages = dose
                        batch2.save()
                    else:
                        bill_prescription = Prescription(
                            date = batch['date'],
                            bill = amount,
                            balance = amount,
                            stashed_amount = 0,
                            category = category,
                            account = request.user,
                            patient = batch['destination'],
                        )
                        bill_prescription.save()
                        batch2.prescription = bill_prescription
                        dose = Dosage(
                            quantity = quantity,
                            frequency = frequency,
                            details = details,
                            unit_cost = unit_cost,
                            prescription = bill_prescription,
                        )
                        dose.save()
                        batch2.dosages = dose
                        batch2.save()
                    batch2_copy = batch2
                    batch2_copy.pk = None
                    batch2_copy.invoice_number = "Prescription"
                    batch2_copy.save()
                    
                    message = f"{batch['stock_item']} has been billed successfully"
                else:
                    message = f"{batch['stock_item']} has already been billed"
                batchForm = StockBatchForm(initial={
                    'destination': batch['destination'],
                    'date':batch['date'],
                    'amount': amount,
                    'invoice_number': 'bill',
                    'pharmacy': "Dispensary",
                    'unit_pack': 1,
                    }) 
                return render(request, 'disp/disp_prescription_bill_prescription.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])& Q(date = batch['date'])),
                    "message":message,
                    "category":category,
                    })
        batchForm = StockBatchForm(initial={
                    'amount': 0,
                    'invoice_number': 'bill',
                    'pharmacy': "Dispensary",
                    'unit_pack': 1,
                    })
        return render(request, 'disp/disp_prescription_bill_prescription.html',{
            'batchForm':batchForm,
        })
    elif action == "prescriptions":
        if request.method == 'GET':
            search = request.GET.get("search","")
            batch = Prescription.objects.filter(patient__icontains = search).exclude(Q(balance__lte = 0)).order_by("-date")
        else:
            batch = Prescription.objects.exclude(Q(balance__lte = 0)).order_by("-date")
        return render(request, 'disp/disp_prescription_prescriptions.html',{
            "batch": batch,
        })
    
def disp_delete(request, action, id):
    if action == "batchItem":
        batch_item = StockBatch.objects.get(id = id)
        invoice = batch_item.invoice_number
        if invoice == 'bill':
            batch_item.prescription.bill -= batch_item.amount
            batch_item.prescription.balance -= batch_item.amount
            batch_item.prescription.save()
        elif invoice =='requisition' and batch_item.amount == 0:
            pass
        elif invoice == 'give_out' or invoice == 'loss':
            batch_item.stock_item.dispensary_quantity += batch_item.unit_pack * batch_item.quantity
        else:
            batch_item.stock_item.dispensary_quantity -= batch_item.unit_pack * batch_item.quantity
        batch_item.stock_item.save()
        StockBatch.objects.get(id = id).delete()
        
        if invoice == 'bill':
            batchForm = StockBatchForm(initial={
                    'destination': batch_item.destination,
                    'date':batch_item.date,
                    'amount': batch_item.amount,
                    'invoice_number': 'bill',
                    'pharmacy': "Dispensary",
                    'unit_pack': 1,
                    }) 
            return render(request, 'disp/disp_prescription_bill_prescription.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = "bill") & Q(pharmacy = 'Dispensary')& Q(destination = batch_item.destination)& Q(date = batch_item.date)),
                    "category":batch_item.prescription.category,
                    })
        
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
            batchForm = StockBatchForm(initial={
                    'invoice_number': 'requisition',
                    'amount': 0,
                    'pharmacy':'Drug Store',
                    'destination':'Dispensary',
                    })
            return render(request, 'disp/disp_stock_request_stock.html',{
                "batchForm":batchForm,
                "batch":StockBatch.objects.filter(Q(invoice_number = 'requisition') & Q(pharmacy = "Drug Store")& Q(destination = 'Dispensary')& Q(amount = 0)),

                })
            
    if action == "bill":
        Prescription.objects.get(id = id).delete()
        return render(request, 'disp/disp_prescription_prescriptions.html',{
            "batch":Prescription.objects.exclude(Q(balance = 0)).order_by("-date"),
        })