from unicodedata import name
from django.urls import path

from stock import views_dsm, views_disp, views_dr
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import FormView
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/login/',LoginView.as_view(template_name="registration/login.html",authentication_form=CustomLoginForm),name='login2'),

    #sample url using slug routing
    #drug store manager urls
    path('dsm_stock/<slug:action>', views_dsm.dsm_stock, name="dsm_stock"),
    path('dsm_accounts/<slug:action>', views_dsm.dsm_accounts, name="dsm_accounts"),
    path('dsm_account/<slug:action>/<int:id>', views_dsm.dsm_account, name="dsm_account"),
    # path('dsm_account/<int:id>', views_dsm.dsm_account, name="dsm_account"),
    path('dsm_reports/<slug:action>', views_dsm.dsm_reports, name="dsm_reports"),
    path('dsm_delete/<slug:action>/<int:id>', views_dsm.dsm_delete, name="dsm_delete"),

    #doctor urls
    path('dr_stock/<slug:action>', views_dr.dr_stock, name="dr_stock"),
    path('dr_prescription/<slug:action>', views_dr.dr_prescription, name="dr_prescription"),
    path('dr_prescription_details/<slug:action>/<int:id>', views_dr.dr_prescription_details, name="dr_prescription_details"),


    #dispenser urls
    path('disp_stock/<slug:action>', views_disp.disp_stock, name="disp_stock"),
    path('disp_reports/<slug:action>', views_disp.disp_reports, name="disp_reports"),
    path('disp_prescription/<slug:action>', views_disp.disp_prescription, name="disp_prescription"),
    path('disp_prescription_details/<slug:action>/<int:id>', views_disp.disp_prescription_details, name="disp_prescription_details"),
    path('disp_delete/<slug:action>/<int:id>', views_disp.disp_delete, name="disp_delete"),
]