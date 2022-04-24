from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from factory.models import Factory, Machine
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
                initial={}
            ),
        })
        return context

    def get_queryset(self):
        queryset = super(FactoryList, self).get_queryset().prefetch_related("machine_set")
        # # category
        # if self.request.GET.get("layer3", None):
        #     queryset = queryset.filter(category=self.request.GET['layer3'])
        #     messages.info(self.request, "layer3={}".format(self.request.GET['layer3']))
        # elif self.request.GET.get("layer2", None):
        #     categories = FactoryCategory.objects.filter(is_active=True, parent_category=self.request.GET['layer2'])
        #     queryset = queryset.filter(category__in=categories)
        #     messages.info(self.request, "layer2={}".format(self.request.GET['layer2']))
        # elif self.request.GET.get("layer1", None):
        #     pcs = FactoryCategory.objects.filter(is_active=True, parent_category=self.request.GET['layer1'])
        #     categories = FactoryCategory.objects.filter(is_active=True, parent_category__in=pcs)
        #     queryset = queryset.filter(category__in=categories)
        #     messages.info(self.request, "layer1={}".format(self.request.GET['layer1']))
        # # materials
        # if self.request.GET.getlist("materials"):
        #     queryset = queryset.filter(machine__materials__in=self.request.GET.getlist("materials"))
        #     messages.info(self.request, "materials={}".format(self.request.GET.getlist('materials')))
        # processes
        if self.request.GET.get("factory_name"):
            queryset = queryset.filter(name__icontains=self.request.GET.get("factory_name"))
        if self.request.GET.get("machine_name"):
            machines = Machine.objects.filter(name__icontains=self.request.GET.get("machine_name"))
            factories = set([m.factory.pk for m in machines])
            queryset = queryset.filter(pk__in=factories)
        return queryset.distinct()


class FactoryDetail(DetailView):
    model = Factory
    template_name = "factory_detail.html"


# class CategoryList(ListView):
#     model = FactoryCategory
#     template_name = "category_list.html"
#     queryset = FactoryCategory.objects.filter(layer=1)


class MachineDetail(DetailView):
    model = Machine
    template_name = "machine_detail.html"
