# coding:utf-8
# from django.conf.urls import url
from django.urls import include, path
from factory.views import FactoryList, FactoryDetail, CategoryList

app_name = 'factory'
urlpatterns = [
    path("", FactoryList.as_view(), name="factory_list"),
    path("<int:pk>", FactoryDetail.as_view(), name="factory_detail"),
    path("category", CategoryList.as_view(), name="category_list"),
]
