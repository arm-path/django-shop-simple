import json
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse, Http404

from app_profile.models import Customer
from .mixins import FilterCategoryMixin
from .models import Category, Product, Specification, CartOrOrder, ProductsInCart


class BaseView(View):
    """ Представление первоначальной страницы """

    @staticmethod
    def get(request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'base.html', {'categories': categories})


class CategoryDetailView(FilterCategoryMixin, View):
    """ Представление категории """

    def get(self, request, *args, **kwargs):
        context = {
            'category': Category.objects.get(slug=self.kwargs['slug']),
            'products': Product.objects.filter(category__slug=self.kwargs['slug']),
            'categories': Category.objects.all(),
            'specifications': Specification.objects.filter(category__slug=self.kwargs['slug'], use_filters=True)
        }
        if request.GET:
            context['products'] = self.get_product(request.GET, context['products'])

        return render(request, 'app_product/category_detail.html', context)


class ProductDetailView(View):
    """ Представление продукта """

    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all(),
            'product': Product.objects.get(slug=self.kwargs['slug'])
        }
        return render(request, 'app_product/product_detail.html', context)


class AddProductToCart(View):
    """ Представление добавления в корзину """

    def post(self, request, *args, **kwargs):
        product_slug = self.kwargs.get('slug') or None
        if not Product.objects.filter(slug=product_slug).exists():
            raise Http404
        if request.user.is_authenticated:
            if not Customer.objects.filter(user=request.user).exists():
                Customer.objects.create(user=request.user)
            customer = Customer.objects.get(user=request.user)
            product = Product.objects.get(slug=product_slug)
            if not CartOrOrder.objects.filter(customer=customer, is_cart=True).exists():
                CartOrOrder.objects.create(customer=customer)
            cart = CartOrOrder.objects.filter(customer=customer, is_cart=True).first()
            product_in_cart = ProductsInCart.objects.create(product=product, cart=cart, total=product.price)
            cart.products.add(product_in_cart)
            cart.sum = cart.sum + product_in_cart.total
            cart.save()

        return redirect('/cart/')


class ChangeQuantityProductToCartView(View):
    """ Представление изменения количества продукта """

    def post(self, request, *args, **kwargs):
        client_data = json.loads(request.body.decode('utf-8'))
        if (client_data.get('quantity') and client_data.get('product_in_cart') and client_data.get('cart') and
                client_data.get('quantity').isdigit() and client_data.get('product_in_cart').isdigit() and
                client_data.get('cart').isdigit()):
            cart = int(client_data.get('cart'))
            product_in_cart = int(client_data.get('product_in_cart'))
            product_in_cart_quantity = int(client_data.get('quantity'))
            if product_in_cart_quantity <= 0:
                return JsonResponse({'error': 'Ошибка в количестве продукта!'})
            if not ProductsInCart.objects.filter(pk=product_in_cart).exists():
                return JsonResponse({'error': 'Продукт не найден!'})
            if not CartOrOrder.objects.filter(pk=cart, is_cart=True).exists():
                return JsonResponse({'error': 'Корзина не найдена!'})
            product_in_cart_model = ProductsInCart.objects.get(pk=product_in_cart)
            cart = CartOrOrder.objects.get(pk=cart)
            product_in_cart_model.quantity = product_in_cart_quantity
            cart.sum = cart.sum - product_in_cart_model.total
            product_in_cart_model.total = product_in_cart_quantity * product_in_cart_model.product.price
            cart.sum = cart.sum + product_in_cart_model.total
            product_in_cart_model.save()
            cart.save()
            return JsonResponse({
                'price': product_in_cart_model.total,
                'sum': cart.sum
            })

        return JsonResponse({'error': 'Получены не правильные данные!'})


class CartView(View):
    """ Представление корзины """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()
        if not Customer.objects.filter(user=request.user).exists():
            Customer.objects.create(user=request.user)
        customer = Customer.objects.get(user=request.user)
        if not CartOrOrder.objects.filter(customer=customer, is_cart=True).exists():
            CartOrOrder.objects.create(customer=customer)
        cart = CartOrOrder.objects.filter(customer=customer, is_cart=True).first()
        context = {
            'categories': Category.objects.all(),
            'cart': cart
        }
        return render(request, 'app_product/cart.html', context)
