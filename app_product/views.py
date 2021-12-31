import json
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from app_profile.models import Customer
from .mixins import FilterCategoryMixin, OrderCheckMixin
from .models import Category, Product, Specification, CartOrOrder, ProductsInCart, Review
from .forms import ReviewForm, OrderForm


class BaseView(View):
    """ Представление первоначальной страницы """

    @staticmethod
    def get(request, *args, **kwargs):
        paginator = Paginator(Product.objects.all(), 6)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {
            'categories': Category.objects.all(),
            'page_obj': page_obj
        }
        return render(request, 'app_product/product_list.html', context)


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
        product = Product.objects.get(slug=self.kwargs['slug'])
        paginator = Paginator(Review.objects.filter(product=product), 2)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {
            'categories': Category.objects.all(),
            'product': product,
            'page_obj': page_obj,
            'page': page
        }
        return render(request, 'app_product/product_detail.html', context)


class ReviewAddView(LoginRequiredMixin, View):
    """ Представление добавления отзыва  """

    login_url = '/profile/authentication/'

    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode('utf-8'))
        rating = str(form_data.get('rating' or None))
        review = str(form_data.get('review' or None))
        if review is not None and rating is not None:
            if not rating.isnumeric():
                return JsonResponse({'errors': 'rating - Должен иметь целочисленный тип данных'})
            rating = int(rating)
            if not rating <= 5 and rating >= 0:
                return JsonResponse({'errors': 'rating - Должен быть в диапазоне от 0-5'})
            if not Customer.objects.filter(user=request.user):
                Customer.objects.create(user=request.user)
            if Review.objects.filter(customer=Customer.objects.get(user=request.user),
                                     product=Product.objects.get(slug=self.kwargs['slug'])).exists():
                return JsonResponse({'error_review': 'Отзыв не добавлен, Вы ранее писали отзыв о продукте!'})
            form_data = ReviewForm({
                'customer': Customer.objects.get(user=request.user).pk,
                'product': Product.objects.get(slug=self.kwargs['slug']),
                'rating': rating, 'review': review
            })
            if form_data.is_valid():
                model_data = form_data.save()
                model_dict = model_to_dict(model_data)
                model_dict['customer'] = request.user.__str__()
                return JsonResponse({'review': model_dict})
        return JsonResponse({'errors': 'Отзыв не добавлен!'})


class ReviewDeleteView(LoginRequiredMixin, View):
    """ Представление уадаления отзыва """

    login_url = '/profile/authentication/'

    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode('utf-8'))
        review = form_data.get('review' or None)
        if not review:
            return JsonResponse({'errors': 'Получены неожиданные данные!'})
        if not review.isnumeric():
            return JsonResponse({'errors': 'Получены неожиданные данные!'})
        customer = customer = Customer.objects.get(user=request.user)
        if Review.objects.filter(pk=review, customer=customer).exists():
            Review.objects.get(pk=review, customer=customer).delete()
            return JsonResponse({'review_delete': review})
        return JsonResponse({'errors': 'Что то пошло не так!'})


class AddProductToCart(LoginRequiredMixin, View):
    """ Представление добавления в корзину """

    login_url = '/profile/authentication/'

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
            if product.product_availability:
                if not cart.products.filter(product=product, cart=cart, total=product.price).exists():
                    product_in_cart = ProductsInCart.objects.create(product=product, cart=cart, total=product.price)
                    cart.products.add(product_in_cart)
                    cart.save()
        return redirect('/cart/')


class ChangeQuantityProductToCartView(LoginRequiredMixin, View):
    """ Представление изменения количества продукта """

    login_url = '/profile/authentication/'

    def post(self, request, *args, **kwargs):
        client_data = json.loads(request.body.decode('utf-8'))
        if not client_data.get('quantity') or not client_data.get('product_in_cart'):
            return JsonResponse({'errors': 'Получены неожиданные данные!'})
        if not client_data.get('quantity').isdigit() or not client_data.get('product_in_cart').isdigit():
            return JsonResponse({'errors': 'Получены неожиданные данные, не известные типы данных!'})
        cart = CartOrOrder.objects.filter(customer__user=request.user, is_cart=True).first()
        product_in_cart = ProductsInCart.objects.filter(pk=client_data.get('product_in_cart')).first()
        product_in_cart_quantity = int(client_data.get('quantity'))
        if product_in_cart_quantity <= 0:
            return JsonResponse({'errors': 'Ошибка в количестве продукта!'})
        if not product_in_cart:
            return JsonResponse({'errors': 'Продукт не найден!'})
        if not cart:
            return JsonResponse({'errors': 'Корзина не найдена!'})
        product_in_cart.quantity = product_in_cart_quantity
        cart.sum = cart.sum - product_in_cart.total
        product_in_cart.total = product_in_cart_quantity * product_in_cart.product.price
        product_in_cart.save()
        cart.save()
        return JsonResponse({
            'price': product_in_cart.total,
            'sum': cart.sum
        })


class DeleteProductToCartView(LoginRequiredMixin, View):
    """ Представление удаления товара из корзины """

    login_url = '/profile/authentication/'

    def post(self, request, *args, **kwargs):
        client_data = json.loads(request.body.decode('utf-8'))
        product_in_cart_id = client_data.get('idProductsInCart' or None)
        cart = CartOrOrder.objects.filter(customer__user=request.user, is_cart=True).first()
        if not product_in_cart_id and not product_in_cart_id.isdigit() and not cart:
            JsonResponse({'errors': 'Получены неожиданные данные!'})
        product_in_cart = ProductsInCart.objects.filter(pk=product_in_cart_id).first()
        if not product_in_cart:
            JsonResponse({'errors': 'Не удалось найти продукт!'})
        if not cart.products.filter(pk=product_in_cart.pk):
            JsonResponse({'errors': 'Не удалось найти продукт в корзине!'})
        cart.products.remove(product_in_cart)
        cart.save()
        return JsonResponse({'product_removed': product_in_cart_id, 'cart_sum_product': cart.sum})


class CartView(LoginRequiredMixin, View):
    """ Представление корзины """

    login_url = '/profile/authentication/'

    def get(self, request, *args, **kwargs):
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


class OrderView(LoginRequiredMixin, OrderCheckMixin, View):
    """ Представление оформление заказа """

    login_url = '/profile/authentication/'

    def get(self, request, *args, **kwargs):
        self.order_check(request.user)
        context = {
            'cart': self.cart,
            'customer': self.customer,
            'order_form': OrderForm
        }
        return render(request, 'app_product/order.html', context)

    def post(self, request, *args, **kwargs):
        self.order_check(request.user)
        order_form = OrderForm(request.POST or None)
        self.form_check(order_form)
        context = {
            'cart': self.cart,
            'customer': self.customer,
            'order_form': order_form
        }
        return render(request, 'app_product/order.html', context)
