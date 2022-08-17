from django.urls import path
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
    name="login"
  ),
  path('logout/', LogoutView.as_view(), name='logout'),
]