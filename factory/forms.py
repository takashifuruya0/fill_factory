import imp
from django import forms
from factory.models import Machine, MachineType, Maker
from django.db.models import fields

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
