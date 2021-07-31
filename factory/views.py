from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from factory.models import Factory, Machine, FactoryCategory
from factory.forms import SearchForm
from django.contrib import messages


class FactoryList(ListView):
    model = Factory
    template_name = "factory_list.html"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "search_form": SearchForm(
                initial={
                    "layer3": self.request.GET.get('layer3', None),
                    "layer2": self.request.GET.get('layer2', None),
                    "layer1": self.request.GET.get('layer1', None),
                    "materials": self.request.GET.getlist("materials"),
                    "processes":self.request.GET.getlist("processes"),
                }
            ),
        })
        return context

    def get_queryset(self):
        queryset = super(FactoryList, self).get_queryset().prefetch_related("machine_set")
        # category
        if self.request.GET.get("layer3", None):
            queryset = queryset.filter(category=self.request.GET['layer3'])
            messages.info(self.request, "layer3={}".format(self.request.GET['layer3']))
        elif self.request.GET.get("layer2", None):
            categories = FactoryCategory.objects.filter(is_active=True, parent_category=self.request.GET['layer2'])
            queryset = queryset.filter(category__in=categories)
            messages.info(self.request, "layer2={}".format(self.request.GET['layer2']))
        elif self.request.GET.get("layer1", None):
            pass
        # materials
        if self.request.GET.getlist("materials"):
            queryset = queryset.filter(machine__materials__in=self.request.GET.getlist("materials"))
            messages.info(self.request, "materials={}".format(self.request.GET.getlist('materials')))
        # processes
        if self.request.GET.getlist("processes"):
            queryset = queryset.filter(machine__processes__in=self.request.GET.getlist("processes"))
            messages.info(self.request, "processes={}".format(self.request.GET.getlist('processes')))
        return queryset


class FactoryDetail(DetailView):
    model = Factory
    template_name = "factory_detail.html"


class CategoryList(ListView):
    model = FactoryCategory
    template_name = "category_list.html"
    queryset = FactoryCategory.objects.filter(layer=1)


class MachineDetail(DetailView):
    model = Machine
    template_name = "machine_detail.html"
