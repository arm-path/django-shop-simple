from django.shortcuts import render
from django.views.generic import View

from .models import Category
from .forms import CategoryForm, SpecificationForm, ValuesOfSpecificationForm


class BaseView(View):
    """ Представление первоначальной страницы """
    
    def get(self, request, *args, **kwarsg):
        return render (request, 'base.html', {})


class CategoryCreateView(View):
    """ Представление создания Категории """

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form_category = CategoryForm()
        form_specification = SpecificationForm()
        form_value = ValuesOfSpecificationForm()
        context = {'form_category': form_category, 
                    'categories': categories,
                    'form_specification': form_specification,
                    'form_value': form_value
        }
        return render(request, 'app_product/category_create.html', context=context)
