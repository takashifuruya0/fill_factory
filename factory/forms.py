import imp
from tkinter import Widget
from django import forms
from factory.models import Machine, MachineType, Maker
from django.db.models import fields


class SpecMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        machine_fields = Machine._meta.get_fields()
        for f in machine_fields:
            if 'spec' in f.name:
                if type(f) in (fields.IntegerField, fields.FloatField):
                    self.fields[f'min_{f.name}'] = forms.IntegerField(
                        required=False, label=f'{f.verbose_name};最小値',
                        widget=forms.NumberInput(attrs={"class": "form-control"}),
                        )
                    self.fields[f'max_{f.name}'] = forms.IntegerField(
                        required=False, label=f'{f.verbose_name};最大値',
                        widget=forms.NumberInput(attrs={"class": "form-control"}),
                        )
                elif type(f) == fields.BooleanField:
                    self.fields[f"{f.name}"] = forms.BooleanField(
                        required=False, label=f.verbose_name,
                        )
                elif type(f) == fields.CharField:
                    self.fields[f"{f.name}"] = forms.CharField(
                        required=False, label=f.verbose_name,
                        widget=forms.TextInput(attrs={"class": "form-control"})
                        )


class MachineSearchForm(SpecMixin, forms.Form):
    machine_name = forms.CharField(
        label='機械名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    machine_types = forms.ModelMultipleChoiceField(
        queryset=MachineType.objects.all(), label='機械種別', required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        )
    makers = forms.ModelMultipleChoiceField(
        queryset=Maker.objects.all(), label='メーカー', required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        )


class FactorySearchForm(SpecMixin, forms.Form):
    factory_name = forms.CharField(
        label='工場名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    is_having_machines = forms.BooleanField(
        label="保有機械データあり", required=False,
        widget=forms.CheckboxInput()
    )
    machine_name = forms.CharField(
        label='機械名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    machine_types = forms.ModelMultipleChoiceField(
        queryset=MachineType.objects.all(), label='機械種別', required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        )
    makers = forms.ModelMultipleChoiceField(
        queryset=Maker.objects.all(), label='メーカー', required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        )