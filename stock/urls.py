from unicodedata import name
from django.urls import path

from stock import views_dsm, views_disp, views_dr
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.index, name="index"),    
    path('register', views.register, name="register"),    
    path('login/', LoginView.as_view(
    authentication_form=CustomLoginForm),
    name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
  
    #sample url using slug routing
    #drug store manager urls
    path('dsm_stock/<slug:action>', views_dsm.dsm_stock, name="dsm_stock"),
    path('dsm_accounts/<slug:action>', views_dsm.dsm_accounts, name="dsm_accounts"),
    path('dsm_reports/<slug:action>', views_dsm.dsm_reports, name="dsm_reports"),

    #doctor urls
    path('dr_stock/<slug:action>', views_dr.dr_stock, name="dr_stock"),
    path('dr_prescription/<slug:action>', views_dr.dr_prescription, name="dr_prescription"),

    #dispenser urls
    path('disp_stock/<slug:action>', views_disp.disp_stock, name="disp_stock"),
    path('disp_reports/<slug:action>', views_disp.disp_reports, name="disp_reports"),
    path('disp_prescription/<slug:action>', views_disp.disp_prescription, name="disp_prescription")
   
]