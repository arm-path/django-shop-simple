from django.urls import path

from .views import BaseView, CategoryDetailView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail')
]