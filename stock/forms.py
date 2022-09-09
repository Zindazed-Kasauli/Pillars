# my_app/forms.py
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from .models import *

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control'}
    )

class CustomSignUpForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control', 'value': '{{user.username}}' }
    )
    self.fields['password1'].widget.attrs.update(
      {'class': 'form-control'}
    )
    self.fields['password2'].widget.attrs.update(
      {'class': 'form-control'}
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2', )
        
class StockBatchForm(forms.ModelForm):
    class Meta:
      model = StockBatch
      fields = ('invoice_number', 'quantity', 'expiry_date', 'amount','date','pharmacy','unit_pack','stock_item','destination')
      widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'expiry_date': forms.TextInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
      super(StockBatchForm, self).__init__(*args, **kwargs)
      self.fields['stock_item'].queryset = self.fields['stock_item'].queryset.order_by('name')
      the_fields = ('invoice_number', 'quantity', 'expiry_date', 'amount','date','pharmacy','unit_pack','stock_item','destination')
      for key in the_fields:
        self.fields[key].widget.attrs.update(
      {'class': 'form-control'}
    )
      
class StockItemForm(forms.ModelForm):
  class Meta:
    model = StockItem
    fields = ('name', 'strength', 'drug_type', 'cat1_price')
    
  def __init__(self, *args, **kwargs):
    super(StockItemForm, self).__init__(*args, **kwargs)
    the_fields = ('name', 'strength', 'drug_type', 'cat1_price')    
    for key in the_fields:
      self.fields[key].widget.attrs.update(
    {'class': 'form-control'}
  )