from django.urls import path

from .views import CategoryCreateView, CategoryChangeView, CategoryDeleteView
from .views import SpecificationCreateView, SpecificationDeleteView, SpecificationChangeView
from .views import ValuesOfSpecificationCreateView, ValueOfSpecificationChangeView, ValueSpecificationDeleteView
from .views import ControlProductView, CreateProductView, ChangeProductView, ChangeCategoryInProductView, ProductDeleteView
from .views import FilterControlView, FilterCreateView
from .views import PickupPointCreateView, PickupPointChangeView, PickupPointDeleteView

urlpatterns = [
    path('category-create', CategoryCreateView.as_view(), name='category_create'),
    path('category-change/<str:slug>/', CategoryChangeView.as_view(), name='category_change'),
    path('category-delete/<str:slug>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('specification-create/<str:slug>/', SpecificationCreateView.as_view(), name='specification_create'),
    path('specification-change/<str:slug>/<int:pk>/', SpecificationChangeView.as_view(), name='specification_change'),
    path('specification-delete/<str:slug>/<int:pk>/', SpecificationDeleteView.as_view(), name='specification_delete'),
    path('specification/<str:slug>/value-create/', ValuesOfSpecificationCreateView.as_view(), name='specification_value_create'),
    path('specification/<str:slug>/value/<int:pk>/', ValueOfSpecificationChangeView.as_view(), name='specification_value_change'),
    path('specification/<str:slug>/value-delete/<int:pk>/', ValueSpecificationDeleteView.as_view(), name='specification_value_delete'),
    path('product-create/', ControlProductView.as_view(), name='product_create_control'),
    path('product-create/category/<str:slug>/', CreateProductView.as_view(), name='product_create'),
    path('product-change/<str:slug>/', ChangeProductView.as_view(), name='product_change'),
    path('specification-for-product/<str:slug>/<int:pk>/', ChangeCategoryInProductView.as_view(), name='specification_for_product'),
    path('product-delete/<str:slug>/', ProductDeleteView.as_view(), name='product_delete'),
    path('filter-control/', FilterControlView.as_view(), name='filter_control'),
    path('filter-create/<str:category>/<str:specification>/', FilterCreateView.as_view(), name='filter_create'),
    path('pickup_point/control/', PickupPointCreateView.as_view(), name='pickup_point_control'),
    path('pickup_point/change/<int:pk>/', PickupPointChangeView.as_view(), name='pickup_point_change'),
    path('pickup_point/delete/<int:pk>/', PickupPointDeleteView.as_view(), name='pickup_point_delete')
]
