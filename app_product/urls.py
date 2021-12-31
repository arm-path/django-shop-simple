from django.urls import path

from .views import (BaseView,
                    CategoryDetailView,
                    ProductDetailView,
                    ReviewAddView,
                    ReviewDeleteView,
                    AddProductToCart,
                    CartView,
                    ChangeQuantityProductToCartView,
                    DeleteProductToCartView,
                    OrderView)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('review/<str:slug>/add/', ReviewAddView.as_view(), name='review_add'),
    path('review/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('add_product/cart/<str:slug>/', AddProductToCart.as_view(), name='product_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/product/delete/', DeleteProductToCartView.as_view(), name='product_to_cart_delete'),
    path('cart/product/change/<int:pk>/quantity/', ChangeQuantityProductToCartView.as_view(), name='product_to_cart_change_quantity'),
    path('order/', OrderView.as_view(), name='order')
]
