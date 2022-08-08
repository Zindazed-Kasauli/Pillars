from django.shortcuts import render, redirect

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
        return render(request, 'dsm/dsm_accounts_new_account.html')
    else: #edit_account
        return render(request, 'dsm/dsm_accounts_edit_account.html')