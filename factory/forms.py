from cProfile import label
from tkinter import Widget
from django import forms
from factory.models import MachineType, Maker


class SearchForm(forms.Form):
    factory_name = forms.CharField(
        label='工場名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    machine_name = forms.CharField(
        label='機械名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    # machine_types = forms.ModelMultipleChoiceField(
    #     queryset=MachineType.objects.all(), label='機械種別',
    #     widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    #     )
    # makers = forms.ModelMultipleChoiceField(
    #     queryset=Maker.objects.all(), label='メーカー',
    #     widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    #     )

