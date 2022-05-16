import imp
from django import forms
from factory.models import Machine, MachineType, Maker
from django.db.models import fields


class MachineSearchForm(forms.Form):
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        machine_fields = Machine._meta.get_fields()
        for f in machine_fields:
            if 'spec' in f.name and type(f) == fields.IntegerField:
                self.fields[f'min_{f.name}'] = forms.IntegerField(
                    required=False, label=f'最小；{f.verbose_name}',
                    widget=forms.NumberInput(attrs={"class": "form-control"}),
                    )
                self.fields[f'max_{f.name}'] = forms.IntegerField(
                    required=False, label=f'最大；{f.verbose_name}',
                    widget=forms.NumberInput(attrs={"class": "form-control"}),
                    )


class FactorySearchForm(MachineSearchForm):
    factory_name = forms.CharField(
        label='工場名', required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
        )
    is_having_machines = forms.BooleanField(
        label="保有機械データあり", required=False,
        widget=forms.CheckboxInput()
    )