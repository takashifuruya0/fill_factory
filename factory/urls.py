# coding:utf-8
# from django.conf.urls import url
from django.urls import include, path
from factory.views import FactoryList, FactoryDetail, MachineDetail
# from factory.views import FactoryList, FactoryDetail, CategoryList, MachineDetail

app_name = 'factory'
urlpatterns = [
    path("", FactoryList.as_view(), name="factory_list"),
    path("<int:pk>", FactoryDetail.as_view(), name="factory_detail"),
    # path("category", CategoryList.as_view(), name="category_list"),
    path("machine/<int:pk>", MachineDetail.as_view(), name="machine_detail"),
]
