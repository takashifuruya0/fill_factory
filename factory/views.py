from django.views.generic import ListView, DetailView, UpdateView, CreateView
from factory.models import Factory, Machine, MachineType, OwnMachine, Maker
from factory.forms import FactorySearchForm, MachineSearchForm
from django.contrib import messages
from django.conf import settings
from django.db.models import fields


class FactoryList(ListView):
    model = Factory
    template_name = "factory_list.html"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        # params
        params = ""
        params_dict = dict()
        search_form = FactorySearchForm(self.request.GET)
        for k, vs in dict(self.request.GET).items():
            if not k == "page":
                name = search_form.fields[k].label
                params_dict[name] = ",".join(vs)
                for v in vs:
                    params = params + "&{}={}".format(k, v)
        if params:
            messages.info(self.request, "検索結果を表示します。{}".format(params))
        # context
        context = super().get_context_data(**kwargs)
        context.update({
            "search_form": search_form,
            "num": self.get_queryset().count(),
            "params": params,
            "params_dict": params_dict,
            "specs": settings.SPECS,
        })
        return context

    def get_queryset(self):
        queryset = super(FactoryList, self).get_queryset()
        if self.request.GET: 
            machine_queryset = Machine.objects.all()
            machine_fields = Machine._meta.get_fields()
            is_query_with_machine = False
            # 工場名
            if self.request.GET.get("factory_name"):
                queryset = queryset.filter(name__icontains=self.request.GET.get("factory_name"))
            # 機械データあり
            if self.request.GET.get("is_having_machines"):
                is_query_with_machine = True
            # spec
            for f in machine_fields:
                if 'spec' in f.name:
                    if type(f) in (fields.IntegerField, fields.FloatField):
                        if self.request.GET.get(f"max_{f.name}"):
                            is_query_with_machine = True
                            machine_queryset = machine_queryset.filter(**{f'{f.name}__lte': self.request.GET.get(f"max_{f.name}")})
                        elif self.request.GET.get(f"min_{f.name}"):
                            is_query_with_machine = True
                            machine_queryset = machine_queryset.filter(**{f'{f.name}__gte': self.request.GET.get(f"min_{f.name}")})
                    elif type(f) == fields.BooleanField and self.request.GET.get(f.name):
                        val = True if self.request.GET.get(f.name) == 'on' else False
                        machine_queryset = machine_queryset.filter(**{f'{f.name}': val})
                    elif type(f) == fields.CharField and self.request.GET.get(f.name):
                        machine_queryset = machine_queryset.filter(**{f'{f.name}__icontains': self.request.GET.get(f.name)})
            # 機械名
            if self.request.GET.get("machine_name"):
                is_query_with_machine = True
                machine_queryset = machine_queryset.filter(name__icontains=self.request.GET.get("machine_name"))
            # 機械種別
            if self.request.GET.getlist("machine_types"):
                machine_queryset = machine_queryset.filter(machine_type__in=self.request.GET.getlist("machine_types"))
            # maker
            if self.request.GET.getlist("makers"):
                machine_queryset = machine_queryset.filter(maker__in=self.request.GET.getlist("makers"))
            # machines
            if is_query_with_machine:
                own_machines = OwnMachine.objects.filter(machine__pk__in=set([m.pk for m in machine_queryset]))
                queryset = queryset.filter(pk__in=set([om.factory.pk for om in own_machines]))
        return queryset.distinct().order_by("-last_updated_at")


class FactoryDetail(DetailView):
    model = Factory
    template_name = "factory_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['own_machines'] = OwnMachine.objects.filter(factory=context['object']).select_related('machine')
        return context


class MachineList(ListView):
    model = Machine
    template_name = "machine_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        params = ""
        params_dict = {}
        search_form = MachineSearchForm(self.request.GET)
        for k, vs in dict(self.request.GET).items():
            if not k == "page":
                name = search_form.fields[k].label
                if k == 'machine_types':
                    params_dict[name] = ",".join([u.name for u in MachineType.objects.filter(pk__in=vs)])
                elif k == 'makers':
                    params_dict[name] = ",".join([u.name for u in Maker.objects.filter(pk__in=vs)])
                else:
                    params_dict[name] = ",".join(vs)
                for v in vs:
                    params = params + "&{}={}".format(k, v)
        # context
        context = super(MachineList, self).get_context_data(**kwargs)
        context.update({
            "search_form": search_form,
            "num": self.get_queryset().count(),
            "params": params,
            "params_dict": params_dict,
            "specs": settings.SPECS,
        })
        return context
    
    def get_queryset(self):
        queryset = super(MachineList, self).get_queryset()
        if self.request.GET: 
            machine_fields = Machine._meta.get_fields()
            # spec
            for f in machine_fields:
                if 'spec' in f.name:
                    if type(f) in (fields.IntegerField, fields.FloatField):
                        if self.request.GET.get(f"max_{f.name}"):
                            queryset = queryset.filter(**{f'{f.name}__lte': self.request.GET.get(f"max_{f.name}")})
                        elif self.request.GET.get(f"min_{f.name}"):
                            queryset = queryset.filter(**{f'{f.name}__gte': self.request.GET.get(f"min_{f.name}")})
                    elif type(f) == fields.BooleanField and self.request.GET.get(f.name):
                        val = True if self.request.GET.get(f.name) == 'on' else False
                        queryset = queryset.filter(**{f'{f.name}': val})
                    elif type(f) == fields.CharField and self.request.GET.get(f.name):
                        queryset = queryset.filter(**{f'{f.name}__icontains': self.request.GET.get(f.name)})
            # 機械名
            if self.request.GET.get("machine_name"):
                queryset = queryset.filter(name__icontains=self.request.GET.get("machine_name"))
            # 機械種別
            if self.request.GET.getlist("machine_types"):
                queryset = queryset.filter(machine_type__in=self.request.GET.getlist("machine_types"))
            # maker
            if self.request.GET.getlist("makers"):
                queryset = queryset.filter(maker__in=self.request.GET.getlist("makers"))
        return queryset.distinct().order_by("-last_updated_at")


class MachineDetail(DetailView):
    model = Machine
    template_name = "machine_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = context['object']._meta.get_fields()
        specs = dict()
        context["specs"] = dict()
        for f in fields:
            if 'spec_' in f.name and f.value_from_object(context['object']):
                specs[f.name] = {
                    'name': f.verbose_name,
                    'value': f.value_from_object(context['object'])
                }
                for i in settings.SPECS:
                    if f"spec_{i}" in f.name and not i in context["specs"].keys():
                        context["specs"][i] = settings.SPECS[i]
        context['specdata'] = specs
        # context["specs"] = settings.SPECS
        return context