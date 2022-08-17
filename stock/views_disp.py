from django.shortcuts import render, redirect

#dispenser stock views
def disp_stock(request, action):
    if action == "request_stock" or action == "stock":
        return render(request, 'disp/disp_stock_request_stock.html')
    elif action == "search_stock":
        return render(request, 'disp/disp_stock_search_stock_item.html')
    elif action == "give_out_stock":
        return render(request, 'disp/disp_stock_give_out_stock.html')
    elif action == "adjustments_losses":
        return render(request, 'disp/disp_stock_adjustments_losses.html')
    elif action == "stock_price_list":
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