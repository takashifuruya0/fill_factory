from django import forms
from factory.models import FactoryCategory, Material, AvailableProcess


class SearchForm(forms.Form):
    layer1 = forms.ModelChoiceField(
        label="大分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=1, is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    layer2 = forms.ModelChoiceField(
        label="中分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=2, is_active=True),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    layer3 = forms.ModelChoiceField(
        label="小分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=3, is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    materials = forms.ModelMultipleChoiceField(
        label="材質", required=False,
        queryset=Material.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    processes = forms.ModelMultipleChoiceField(
        label="対応加工", required=False,
        queryset=AvailableProcess.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

