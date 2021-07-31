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
                initial={"layer3": self.request.GET.get('layer3', None)}
            ),
        })
        return context

    def get_queryset(self):
        queryset = super(FactoryList, self).get_queryset()
        if self.request.GET.get("layer3", None):
            queryset = queryset.filter(category=self.request.GET['layer3'])
            messages.info(self.request, "layer3={}".format(self.request.GET['layer3']))
        return queryset


class FactoryDetail(DetailView):
    model = Factory
    template_name = "factory_detail.html"


class CategoryList(ListView):
    model = FactoryCategory
    template_name = "category_list.html"
    queryset = FactoryCategory.objects.filter(layer=1)
