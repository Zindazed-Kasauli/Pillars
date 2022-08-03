from unicodedata import name
from django.urls import path

from stock import views_dsm
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.index, name="index"),    
    path('register', views.register, name="register"),    
    path('log_out', views.log_out, name="log_out"),    
    path('login/', LoginView.as_view(
    authentication_form=CustomLoginForm),
    name="login"),
  
    #sample url using slug routing
    path('drug_store_manager/', views_dsm.drug_store_manager, name="drug_store_manager")

]