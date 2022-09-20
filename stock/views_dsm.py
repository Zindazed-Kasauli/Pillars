from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.db.models import Q, Sum, F
from datetime import datetime

#drug store manager stock_views 
def dsm_stock(request, action):
    if action == "search_stock_item":
        items = StockItem.objects.all().order_by('name')
        if request.method == "GET":
            search = request.GET.get("search","")
            items = StockItem.objects.filter(name__icontains = search).order_by('name')
        if request.method == "POST":
            item_id = request.POST["itemid"]
            cat1 = request.POST["cat1"]
            item = StockItem.objects.get(id = item_id)
            item.cat1_price = cat1
            item.save()
        return render(request, 'dsm/dsm_stock_search_stock_item.html',{'items':items})
    elif action == "requisitions":
        message = ""
        if request.method == "POST":
            item_id = int(request.POST['item_id'])
            item = StockBatch.objects.get(id = item_id)
            if item.amount == 0:
                item.stock_item.dispensary_quantity += item.unit_pack * item.quantity
                item.stock_item.store_quantity -= item.unit_pack * item.quantity
                item.stock_item.save()
                item.dispensary_quantity = item.stock_item.dispensary_quantity
                item.store_quantity = item.stock_item.store_quantity
                item.amount = 1
                item.save()
                message = f"{item.stock_item} request accepted"
            else:
                message = f"{item.stock_item} request was already accepted"
        return render(request, 'dsm/dsm_stock_requisitions.html',{
                    "batch":StockBatch.objects.filter(Q(invoice_number = 'requisition') & Q(pharmacy = "Drug Store")& Q(destination = 'Dispensary')& Q(amount = 0)),
                    "message":message,
                    })
    elif action == "give_out_stock":
        if request.method == "POST":
            form = StockBatchForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    form.cleaned_data['stock_item'].store_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.store_quantity = form.cleaned_data['stock_item'].store_quantity
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
                    'pharmacy': "Drug Store",
                    }) 
                return render(request, 'dsm/dsm_stock_give_out_stock.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])),
                    "message":message,
                    })
        batchForm = StockBatchForm(initial={
                    'amount': 0,
                    'invoice_number': 'give_out',
                    'pharmacy': "Drug Store",
                    })
        return render(request, 'dsm/dsm_stock_give_out_stock.html',{
            'batchForm':batchForm,
        })
    elif action == "stock_price_list":
        return redirect('dsm_stock','search_stock_item')
        return render(request, 'dsm/dsm_stock_stock_price_list.html')
    elif action == "stock_batches":
        if request.method == 'GET':
            batch_type = request.GET.get('batch_type',False)
            batch = StockBatch.objects.all()
            if batch_type == 'added':
                batch = StockBatch.objects.filter(destination = 'Drug Store').exclude(invoice_number = 'adjustment')
            elif batch_type == 'requested':
                batch = StockBatch.objects.filter(invoice_number = 'requisition')
            elif batch_type == 'given_out':
                batch = StockBatch.objects.filter(invoice_number = 'give_out')
            elif batch_type == 'adjusted':
                batch = StockBatch.objects.filter(invoice_number = 'adjustment')
            elif batch_type == 'lost':
                batch = StockBatch.objects.filter(invoice_number = 'loss')
            elif batch_type == 'dispensed':
                batch = StockBatch.objects.filter(invoice_number = 'dispensation')
        return render(request, 'dsm/dsm_stock_stock_batches.html',{
            'batch':batch,
        })
    elif action == "adjustments":
        if request.method == "GET":
            form = StockBatchForm(request.GET)
            if form.is_valid():
                batch = form.cleaned_data
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    form.cleaned_data['stock_item'].store_quantity += form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.store_quantity = form.cleaned_data['stock_item'].store_quantity
                    batch.save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} added"
                else:
                    message = f"{batch['stock_item']} has already been added"
                batchForm_a = StockBatchForm(initial={
                    'destination': 'Drug Store',
                    'date':batch['date'],
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    }) 
                batchForm_l = StockBatchForm(initial={
                    'pharmacy': "Drug Store",
                    'amount': 0,
                    'invoice_number': 'loss',
                    })
                return render(request, 'dsm/dsm_stock_adjustments_losses.html',{
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
                    form.cleaned_data['stock_item'].store_quantity -= form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.store_quantity = form.cleaned_data['stock_item'].store_quantity
                    batch.save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} removed as loss"
                else:
                    message = f"{batch['stock_item']} has already been removed as loss"
                batchForm_l = StockBatchForm(initial={
                    'pharmacy': 'Drug Store',
                    'date':batch['date'],
                    'amount': 0,
                    'invoice_number': 'loss',
                    }) 
                batchForm_a = StockBatchForm(initial={
                    'destination': "Drug Store",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
                return render(request, 'dsm/dsm_stock_adjustments_losses.html',{
                    "batchForm_l":batchForm_l,
                    "batchForm_a":batchForm_a,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])& Q(destination = batch['destination'])),
                    "message":message,
                    })
        batchForm_a = StockBatchForm(initial={
                    'destination': "Drug Store",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
        batchForm_l = StockBatchForm(initial={
                    'pharmacy': "Drug Store",
                    'amount': 0,
                    'invoice_number': 'loss',
                    })
        return render(request, 'dsm/dsm_stock_adjustments_losses.html',{
            'batchForm_l':batchForm_l,
            'batchForm_a':batchForm_a,
        })
    elif action == "add_stock_item" or action == "stock":
        #addition of a new stock
        if request.method == "GET":
            form = StockItemForm(request.GET)
            pharmacy = request.GET.get('pharmacy',False)
            invoice_number = request.GET.get('invoice_number',False)
            date = request.GET.get('date',False)
            if date:
                date = datetime.strptime(date, "%Y-%m-%d")
                date = date.date()
            
            if form.is_valid():
                item = form.cleaned_data
                if not StockItem.objects.filter(Q(name = form.cleaned_data["name"]) & Q(strength = form.cleaned_data["strength"]) & Q(drug_type = form.cleaned_data["drug_type"])).exists():
                    item = form.save(commit=False)
                    item.account = request.user
                    item.destination = "Drug Store"
                    item.save()
                    message = f"{item.name} added successfully"
                else:
                    message = f"{item['name']} already exists"
                
                itemForm = StockItemForm()
                if pharmacy:
                    batchForm = StockBatchForm(initial={
                    'invoice_number': invoice_number,
                    'pharmacy':pharmacy,
                    'date':date
                    }) 
                    return render(request, 'dsm/dsm_stock_add_stock_item.html',{
                        "batchForm":batchForm,
                        "itemForm":itemForm,
                        "message":message,
                        "batch":StockBatch.objects.filter(Q(invoice_number = invoice_number) & Q(pharmacy = pharmacy)),
                        })
                else:
                    batchForm = StockBatchForm()
                    return render(request, 'dsm/dsm_stock_add_stock_item.html',{
                        "batchForm":batchForm,
                        "itemForm":itemForm,
                        "message":message,
                        })
        
        #addition of invoice item(batch item)
        if request.method == "POST":
            form = StockBatchForm(request.POST)
            if form.is_valid():
                batch = form.cleaned_data
                print(type(form.cleaned_data['stock_item']))
                print(form.cleaned_data['stock_item'].name)
                if not StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy']) & Q(stock_item = batch['stock_item'])).exists():
                    batch = form.save(commit=False)
                    batch.account = request.user
                    batch.destination = "Drug Store"
                    form.cleaned_data['stock_item'].store_quantity += form.cleaned_data['unit_pack'] * form.cleaned_data['quantity']
                    form.cleaned_data['stock_item'].save()
                    batch.store_quantity = form.cleaned_data['stock_item'].store_quantity                    
                    batch.save()
                    batch = form.cleaned_data
                    message = f"{batch['stock_item']} added to the batch"
                else:
                    message = f"{batch['stock_item']} already exists in the batch"
                itemForm = StockItemForm()
                batchForm = StockBatchForm(initial={
                    'invoice_number': batch['invoice_number'],
                    'pharmacy':batch['pharmacy'],
                    'date':batch['date']
                    }) 
                return render(request, 'dsm/dsm_stock_add_stock_item.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = batch['invoice_number']) & Q(pharmacy = batch['pharmacy'])),
                    "message":message,
                    })
        batchForm = StockBatchForm()
        itemForm = StockItemForm()
        return render(request, 'dsm/dsm_stock_add_stock_item.html',{
            "batchForm":batchForm,
            "itemForm":itemForm
            })
    else:
        pass

#drug store manager report_views
def dsm_reports(request, action):
    if action == "periodic_reports":
        if request.method == 'POST':
            start = request.POST['start']
            stop = request.POST['stop']
            items = []
            
            if start<=stop:
                for stock_item in StockItem.objects.all():
                    if StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = stop)).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').exists():
                        item = dict()
                        item['item'] = stock_item
                        if StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = start)).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').exists():
                            item['start'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = start)).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').first().store_quantity
                        else:
                            item['start'] = 0
                        item['stop'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = stop)).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').first().store_quantity
                        try:
                            item['quantity_received'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = stop) & Q(date__gte = start)).exclude(Q(pharmacy = 'Dispensary') | Q(invoice_number = 'requisition')| Q(invoice_number = 'give_out')| Q(invoice_number = 'loss')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                        except AttributeError:
                            item['quantity_received'] = 0
                        try:
                            item['quantity_taken'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = stop) & Q(date__gte = start) & (Q(invoice_number = 'requisition')| Q(invoice_number = 'give_out')| Q(invoice_number = 'loss'))).exclude(Q(pharmacy = 'Dispensary')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                        except AttributeError:
                            item['quantity_taken'] = 0
                        items.append(item)
                        
            return render(request, 'dsm/dsm_reports_periodic_reports.html',{'items':items})
        return render(request, 'dsm/dsm_reports_periodic_reports.html')
    elif action == "notifications":
        green = StockItem.objects.filter(Q(store_quantity__lte = 100) & Q(store_quantity__gt = 40))
        yellow = StockItem.objects.filter(Q(store_quantity__lte = 40) & Q(store_quantity__gt = 5))
        red = StockItem.objects.filter(Q(store_quantity__lte = 5))
        return render(request, 'dsm/dsm_reports_notifications.html',{
            'green':green,
            'yellow':yellow,
            'red':red,
        })
    elif action == "daily_report" or action == "reports":
        items = []
        for stock_item in StockItem.objects.all():
            if StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').exists():
                item = dict()
                item['item'] = stock_item
                item['start'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Dispensary')).order_by('date').first().store_quantity
                item['stop'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date())& Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Dispensary')).order_by('-date').first().store_quantity
                try:
                    item['quantity_received'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date()) & Q(date__gte = datetime.today().date())).exclude(Q(pharmacy = 'Dispensary') | Q(invoice_number = 'requisition')| Q(invoice_number = 'give_out')| Q(invoice_number = 'loss')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                except AttributeError:
                    item['quantity_received'] = 0
                try:
                    item['quantity_taken'] = StockBatch.objects.filter(Q(stock_item = stock_item) & Q(date__lte = datetime.today().date()) & Q(date__gte = datetime.today().date()) &( Q(invoice_number = 'requisition')| Q(invoice_number = 'give_out')| Q(invoice_number = 'loss'))).exclude(Q(pharmacy = 'Dispensary')).aggregate(total=Sum(F('quantity') * F('unit_pack')))['total']
                except AttributeError:
                    item['quantity_taken'] = 0
                items.append(item)
        return render(request, 'dsm/dsm_reports_daily_report.html',{'items':items})
    else:
        pass

#drug store manager accounts views

# if not request.user.is_authenticated:
#         return redirect('login')

def dsm_accounts(request, action):
    if action == "new_account" or action == "accounts":
        # registration page view
        if request.method == 'POST':
            role = request.POST['role']
            print(role)
            #userCreationForm is a default registration form for creating new user
            form = UserCreationForm(request.POST)

            if form.is_valid():
                account = form.save(commit=False)
                account.first_name= role
                account.save()
                users = User.objects.all()
                return render(request, 'dsm/dsm_accounts_edit_account.html',{
                    'users':users,
                    "added":"added"
                    })
        else:
            #nothing happens
            form = UserCreationForm()
        
        context = {'form':form}
        return render(request, 'dsm/dsm_accounts_new_account.html', context)
    else: #edit_account
        users = User.objects.all()
        return render(request, 'dsm/dsm_accounts_edit_account.html', {'users':users})
    
def dsm_account(request, action, id):
    if action == "edit_account":
        user = User.objects.get(id = id)
        if request.method == 'POST':
            username = request.POST['username']
            role = request.POST['role']
            #userChangeForm is a default registration form for changing new user credentials
            # form = UserChangeForm(request.POST, instance=user)
            form2 = PasswordChangeForm(data = request.POST, user=user)
            if form2.is_valid():
                user.username = username
                user.first_name = role
                user.save()
                form2.save()
                users = User.objects.all()
                return render(request, 'dsm/dsm_accounts_edit_account.html',{
                    'users':users,
                    "added":"changed"
                    })
        else:
            #nothing happens
            # form = UserChangeForm(instance =user)
            form2 = PasswordChangeForm(user = user)
        
        context = {
            'form2':form2,
            'user':user
            }
        return render(request, 'dsm/dsm_accounts_edit_account_details.html', context)
    if action == "explode_account":
        user = User.objects.get(id = id)
        return render(request, 'dsm/dsm_accounts_edit_account_details.html', {'user':user} )
    
def dsm_delete(request, action, id):
    if action == "user":
        User.objects.get(id = id).delete()
        return redirect(dsm_accounts,"edit_account")
    if action == "batchItem":
        batch_item = StockBatch.objects.get(id = id)
        invoice = batch_item.invoice_number
        if invoice == 'give_out' or invoice == 'loss':
            batch_item.stock_item.store_quantity += batch_item.unit_pack * batch_item.quantity
        else:
            batch_item.stock_item.store_quantity -= batch_item.unit_pack * batch_item.quantity
        batch_item.stock_item.save()
        StockBatch.objects.get(id = id).delete()
        
        if invoice == 'loss' or invoice == 'adjustment':
            batchForm_a = StockBatchForm(initial={
                    'destination': "Drug Store",
                    'amount': 0,
                    'invoice_number': 'adjustment',
                    })
            batchForm_l = StockBatchForm(initial={
                        'pharmacy': "Drug Store",
                        'amount': 0,
                        'invoice_number': 'loss',
                        })
            return render(request, 'dsm/dsm_stock_adjustments_losses.html',{
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
                return render(request, 'dsm/dsm_stock_give_out_stock.html',{
                    "batchForm":batchForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = 'give_out') & Q(pharmacy = batch_item.pharmacy)& Q(destination = destination)),
                    })
            else:
                batchForm = StockBatchForm()
                return render(request, 'dsm/dsm_stock_give_out_stock.html',{
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
                return render(request, 'dsm/dsm_stock_add_stock_item.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    "batch":StockBatch.objects.filter(Q(invoice_number = invoice_number) & Q(pharmacy = pharmacy)),
                    })
            else:
                batchForm = StockBatchForm()
                return render(request, 'dsm/dsm_stock_add_stock_item.html',{
                    "batchForm":batchForm,
                    "itemForm":itemForm,
                    })