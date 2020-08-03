from django import forms
from django.core.validators import MinValueValidator

from .models import CATEGORY_CHOICES

default_category = CATEGORY_CHOICES[0][0]



class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Название')
    description = forms.TimeField(max_length=2000, label='Текст', widget=forms.Textarea)
    category = forms.ChoiceField(max_lenght=20, choices=CATEGORY_CHOICES, initial=default_category, label='Категория')
    amount = forms.IntegerField (label='Остаток',validators= (MinValueValidator(0)))
    price =  forms.DecimalField(label= 'Цена', max_digits=7, decimal_places=2,validators= (MinValueValidator(0)))
