from django.urls import path

from .views import BaseView, CategoryCreateView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category-create', CategoryCreateView.as_view(), name='category_create')
]