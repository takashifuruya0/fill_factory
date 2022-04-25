from django.views.generic import ListView, DetailView, UpdateView, CreateView
from factory.models import Factory, Machine, OwnMachine
from factory.forms import SearchForm
from django.contrib import messages
from django.db.models import fields


class FactoryList(ListView):
    model = Factory
    template_name = "factory_list.html"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "search_form": SearchForm(self.request.GET),
        })
        if self.request.GET:
            for k, v in self.request.GET.dict().items():
                if not v == '':
                    print(f'{k}={v}')
        return context

    def get_queryset(self):
        queryset = super(FactoryList, self).get_queryset()
        if self.request.GET:
            machine_queryset = Machine.objects.all()
            machine_fields = Machine._meta.get_fields()
            for f in machine_fields:
                if 'spec' in f.name and type(f) == fields.IntegerField:
                    if self.request.GET.get(f"max_{f.name}"):
                        machine_queryset = machine_queryset.filter(**{f'{f.name}__lte': self.request.GET.get(f"max_{f.name}")})
                    elif self.request.GET.get(f"min_{f.name}"):
                        machine_queryset = machine_queryset.filter(**{f'{f.name}__gte': self.request.GET.get(f"min_{f.name}")})
            if self.request.GET.get("factory_name"):
                queryset = queryset.filter(name__icontains=self.request.GET.get("factory_name"))
            if self.request.GET.get("machine_name"):
                machine_queryset = machine_queryset.filter(name__icontains=self.request.GET.get("machine_name"))
            # machines
            own_machines = OwnMachine.objects.filter(machine__pk__in=set([m.pk for m in machine_queryset]))
            queryset = queryset.filter(pk__in=set([om.factory.pk for om in own_machines]))
        return queryset.distinct()


class FactoryDetail(DetailView):
    model = Factory
    template_name = "factory_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['own_machines'] = OwnMachine.objects.filter(factory=context['object']).select_related('machine')
        return context


# class CategoryList(ListView):
#     model = FactoryCategory
#     template_name = "category_list.html"
#     queryset = FactoryCategory.objects.filter(layer=1)


class MachineDetail(DetailView):
    model = Machine
    template_name = "machine_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = context['object']._meta.get_fields()
        specs = dict()
        for f in fields:
            if 'spec' in f.name:
                specs[f.verbose_name] = f.value_from_object(context['object'])
        context['specs'] = specs
        return context