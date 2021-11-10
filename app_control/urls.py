from django.urls import path

from .views import CategoryCreateView, CategoryChangeView
from .views import SpecificationCreateView, SpecificationDeleteView, SpecificationChangeView
from .views import ValuesOfSpecificationCreateView, ValueOfSpecificationChangeView, ValueSpecificationDeleteView
from .views import ControlProductView, CreateProductView

urlpatterns = [
    path('category-create', CategoryCreateView.as_view(), name='category_create'),
    path('category-change/<str:slug>/', CategoryChangeView.as_view(), name='category_change'),
    path('specification-create/<str:slug>/', SpecificationCreateView.as_view(), name='specification_create'),
    path('specification-change/<str:slug>/<int:pk>/', SpecificationChangeView.as_view(), name='specification_change'),
    path('specification-delete/<str:slug>/<int:pk>/', SpecificationDeleteView.as_view(), name='specification_delete'),
    path('specification/<str:slug>/value-create/', ValuesOfSpecificationCreateView.as_view(), name='specification_value_create'),
    path('specification/<str:slug>/value/<int:pk>/', ValueOfSpecificationChangeView.as_view(), name='specification_value_change'),
    path('specification/<str:slug>/value-delete/<int:pk>/', ValueSpecificationDeleteView.as_view(), name='specification_value_delete'),
    path('product-create/', ControlProductView.as_view(), name='product_create_control'),
    path('product-create/category/<str:slug>/', CreateProductView.as_view(), name='product_create')
]
