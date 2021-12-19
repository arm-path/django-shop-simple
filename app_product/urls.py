from django.urls import path

from .views import (BaseView,
                    CategoryDetailView,
                    ProductDetailView,
                    ReviewDeleteView,
                    AddProductToCart,
                    CartView,
                    ChangeQuantityProductToCartView)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('review/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('add_product/cart/<str:slug>/', AddProductToCart.as_view(), name='product_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/product/change/<int:pk>/quantity/', ChangeQuantityProductToCartView.as_view(), name='product_to_cart_change_quantity')
]
