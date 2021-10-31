from django.urls import path

from .views import BaseView, CategoryCreateView, CategoryChangeView, SpecificationCreateView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category-create', CategoryCreateView.as_view(), name='category_create'),
    path('category-change/<str:slug>/', CategoryChangeView.as_view(), name='category_change'),
    path('specification-create/<str:slug>/', SpecificationCreateView.as_view(), name='specification_create')
]
