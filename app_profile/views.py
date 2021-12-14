from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import View

from app_product.models import Category
from .forms import CreateUserForm, ChangeUserForm, CreateCustomerForm, AuthenticationUserForm
from .models import Customer


class CreateProfileView(View):
    """ Представление регистрации пользователя-покупателя """

    def get(self, request, *args, **kwargs):
        context = {'categories': Category.objects.all(),
                   'user_form': CreateUserForm,
                   'customer_form': CreateCustomerForm}
        return render(request, 'app_profile/create_profile.html', context)

    def post(self, request, *args, **kwargs):
        user_form = CreateUserForm(request.POST)
        customer_form = CreateCustomerForm(request.POST, files=request.FILES)
        if user_form.is_valid():
            if customer_form.is_valid():
                user_model = user_form.save()
                customer_model = customer_form.save()
                customer_model.user = user_model
                customer_model.save()
                return redirect('authentication')
        context = {
            'categories': Category.objects.all(),
            'user_form': user_form,
            'customer_form': customer_form
        }
        return render(request, 'app_profile/create_profile.html', context)


class AuthenticationUserView(View):
    """ Представление авторизации пользвателя-покупателя """

    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all(),
            'user_form': AuthenticationUserForm()
        }
        return render(request, 'app_profile/authentication_user.html', context)

    def post(self, request, *args, **kwargs):
        authentication_form = AuthenticationUserForm(data=request.POST)
        if authentication_form.is_valid():
            user = authentication_form.get_user()
            login(request, user)
            return redirect('base')
        context = {
            'categories': Category.objects.all(),
            'user_form': authentication_form
        }
        return render(request, 'app_profile/authentication_user.html', context)


class DetailProfileView(View):
    """ Представление профиля пользователя-покупателя """

    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all()
        }
        return render(request, 'app_profile/detail_profile.html', context)


class ChangeProfileView(View):
    """ Представление изменение профиля пользователя """

    def get(self, request, *args, **kwargs):
        if not Customer.objects.filter(user=request.user).exists():
            Customer.objects.create(user=request.user)
        customer = Customer.objects.get(user=request.user)

        context = {
            'categories': Category.objects.all(),
            'user_form': ChangeUserForm(instance=request.user),
            'customer_form': CreateCustomerForm(instance=customer)
        }
        return render(request, 'app_profile/change_profile.html', context)

    def post(self, request, *args, **kwargs):
        if not Customer.objects.filter(user=request.user).exists():
            Customer.objects.create(user=request.user)
        user_form = ChangeUserForm(request.POST, instance=request.user)
        customer = Customer.objects.get(user=request.user)
        customer_form = CreateCustomerForm(request.POST, instance=customer, files=request.FILES)
        if user_form.is_valid():
            if customer_form.is_valid():
                user_form.save()
                customer_form.save()
                return redirect('detail_profile')
        context = {
            'categories': Category.objects.all(),
            'user_form': user_form,
            'customer_form': customer_form
        }
        return render(request, 'app_profile/change_profile.html', context)
