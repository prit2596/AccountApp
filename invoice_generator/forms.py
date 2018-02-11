from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.admin import widgets

class PartyNamesForm(ModelForm):
    joining_date = forms.DateField(widget = forms.SelectDateWidget())
    class Meta:
        model = Party
        fields = [
            'name',
            'joining_date',
            'contact',
            'address',
        ]
     #   widgets = [
      #      'joining_date' : date
      #  ]

class AccountForm(ModelForm):
    date = forms.DateField(widget = forms.SelectDateWidget())
    class Meta:
        model = Accounts
        fields = [
            'item',
            'date',
            'vehicle_no',
            'challan_no',
            'quantity',
            'rate',
        ]