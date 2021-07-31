from django import forms
from factory.models import FactoryCategory


class SearchForm(forms.Form):
    layer1 = forms.ModelChoiceField(
        label="大分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=1, is_active=True)
    )
    layer2 = forms.ModelChoiceField(
        label="中分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=2, is_active=True)
    )
    layer3 = forms.ModelChoiceField(
        label="小分類", required=False,
        queryset=FactoryCategory.objects.filter(layer=3, is_active=True)
    )
