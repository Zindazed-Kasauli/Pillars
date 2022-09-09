from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# home page view

def index(request):
    #redirects user to login if not logged in
    if not request.user.is_authenticated:
        return redirect('login2')
    elif request.user.first_name == "Drug Store Manager":
        return redirect('dsm_stock',"add_stock_item")
    elif request.user.first_name == "Doctor":
        return redirect('dr_stock','search_stock_item')
    elif request.user.first_name == "Dispenser":
        return redirect('disp_stock','request_stock')

