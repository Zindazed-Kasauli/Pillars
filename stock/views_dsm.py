from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *


#drug store manager stock_views 
def dsm_stock(request, action):
    if action == "search_stock_item":
        return render(request, 'dsm/dsm_stock_search_stock_item.html')
    elif action == "requisitions":
        return render(request, 'dsm/dsm_stock_requisitions.html')
    elif action == "give_out_stock":
        return render(request, 'dsm/dsm_stock_give_out_stock.html')
    elif action == "stock_price_list":
        return render(request, 'dsm/dsm_stock_stock_price_list.html')
    elif action == "stock_batches":
        return render(request, 'dsm/dsm_stock_stock_batches.html')
    elif action == "adjustments":
        return render(request, 'dsm/dsm_stock_adjustments_losses.html')
    elif action == "add_stock_item" or action == "stock":
        return render(request, 'dsm/dsm_stock_add_stock_item.html')
    else:
        pass

#drug store manager report_views
def dsm_reports(request, action):
    if action == "periodic_reports":
        return render(request, 'dsm/dsm_reports_periodic_reports.html')
    elif action == "notifications":
        return render(request, 'dsm/dsm_reports_notifications.html')
    elif action == "daily_report" or action == "reports":
        return render(request, 'dsm/dsm_reports_daily_report.html')
    else:
        pass

#drug store manager accounts views
def dsm_accounts(request, action):
    if action == "new_account" or action == "accounts":
        # registration page view
        if request.method == 'POST':
            role = request.POST['role']
            #userCreationForm is a default registration form for creating new user
            form = UserCreationForm(request.POST)

            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']

                user = User.objects.get(username = username)
                new_account = Account(
                    user = user,
                    role = role,
                )
                new_account.save()
                # password = form.cleaned_data['password1']


                # #authenticates user
                # user = authenticate(username=username, password=password)

                # #logins in user
                # login(request, user)

                # #redirects user to home page
                # return redirect('index')
                return render(request, 'dsm/dsm_accounts_edit_account.html')
        else:
            #nothing happens
            form = UserCreationForm()
        
        context = {'form':form}
        return render(request, 'dsm/dsm_accounts_new_account.html', context)
    else: #edit_account
        return render(request, 'dsm/dsm_accounts_edit_account.html')