from django.shortcuts import render
from django.views.generic import View

from .mixins import FilterCategoryMixin
from .models import Category, Product, Specification


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
