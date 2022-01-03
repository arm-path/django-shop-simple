from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages

from app_product.models import Category, Specification, ValuesOfSpecification, Product, PickUpPoints
from .forms import SpecificationForm, ValuesOfSpecificationForm, ProductAdditionallyForm


class BaseMixin:
    def check_options(self, slug_model='Category', id_model='Specification'):
        self.slug_option = self.kwargs.get('slug')
        self.id_option = self.kwargs.get('pk')
        if self.slug_option:
            if slug_model == 'Category' and not Category.objects.filter(slug=self.slug_option).exists():
                raise Http404()
            if slug_model == 'Specification' and not Specification.objects.filter(slug=self.slug_option).exists():
                raise Http404()
            if slug_model == 'Product' and not Product.objects.filter(slug=self.slug_option).exists():
                raise Http404()
        if self.id_option:
            if id_model == 'Category' and not Category.objects.filter(id=self.id_option).exists():
                raise Http404()
            if id_model == 'Specification' and not Specification.objects.filter(id=self.id_option).exists():
                raise Http404()
            if id_model == 'ValueSpecification' and not ValuesOfSpecification.objects.filter(id=self.id_option).exists():
                raise Http404()
            if id_model == 'Product' and not Product.objects.filter(id=self.id_option).exists():
                raise Http404()


class CategoryChangeMixin(BaseMixin):
    def get_context(self):
        self.check_options()
        categories = Category.objects.all()
        self.model_category = Category.objects.get(slug=self.slug_option)
        specifications = Specification.objects.filter(category=self.model_category)
        form_specification = SpecificationForm()
        context = {
            'slug_category': self.slug_option,
            'category': self.model_category.title,
            'categories': categories,
            'specifications': specifications,
            'form_specification': form_specification
        }
        return context


class SpecificationCreateAndChangeMixin(BaseMixin):
    def get_form_data(self, client_data=None):
        self.check_options()
        form_data = {}
        if client_data:
            if client_data['title'] and client_data['type_filter']:
                form_data = {
                    'title': client_data['title'],
                    'category': Category.objects.get(slug=self.slug_option).pk,
                    'unit': client_data['unit'],
                    'use_filters': client_data['use_filters'],
                    'type_filter': client_data['type_filter']
                }
        return form_data


class ValuesOfSpecificationCreateAndChangeMixin(BaseMixin):
    def get_context(self):
        self.check_options(slug_model='Specification')
        categories = Category.objects.all()
        values_specification = ValuesOfSpecification.objects.filter(specification__slug=self.slug_option)

        form_value_specification = ValuesOfSpecificationForm()
        context = {
            'slug_specification': self.slug_option,
            'form_value_specification': form_value_specification,
            'categories': categories, 'values_specification': values_specification,
            'specification': Specification.objects.get(slug=self.slug_option)
        }
        return context

    def get_form_data(self, client_data=None):
        self.check_options(slug_model='Specification', id_model='ValueSpecification')
        form_data = {}
        if client_data:
            if client_data['value']:
                form_data = {
                    'specification': Specification.objects.get(slug=self.slug_option).pk,
                    'value': client_data['value']
                }
        return form_data


class CreateAndChangeProductMixin(BaseMixin):

    def get_context(self, slug_model=None):
        self.check_options(slug_model=slug_model)
        category = None
        context = None
        if slug_model == 'Category':
            category = Category.objects.get(slug=self.slug_option)
        if slug_model == 'Product':
            self.model_product = Product.objects.get(slug=self.slug_option)
            category = self.model_product.category
        if category:
            specifications = Specification.objects.filter(category=category)
            category_specification = []
            if slug_model == 'Product':
                value_specification_model = [value for value in self.model_product.specification.all().values('specification', 'pk')]
            for specification in specifications:
                if slug_model == 'Product':
                    value_specification = ValuesOfSpecification.objects.filter(specification=specification)
                    select = [value['pk'] for value in value_specification_model if value['specification'] == specification.pk]
                    value = value_specification.values('pk', 'value')
                if slug_model == 'Category':
                    select = None
                    value = ValuesOfSpecification.objects.filter(specification=specification).values('pk', 'value')
                category_specification.append({
                    'pk': specification.pk,
                    'title': specification.title,
                    'slug': specification.slug,
                    'values': value,
                    'select': select[0] if select else None
                })
            context = {
                'form_value_specification': ValuesOfSpecificationForm(),
                'category_specification': category_specification
            }
            if slug_model == 'Product':
                context['slug_product'] = self.slug_option
            if slug_model == 'Category':
                context['category'] = category
        return context

    def get_post_general(self, request=None, action=None, form_product=None):
        if action == 'change':
            self.check_options(slug_model='Product')
        else:
            self.check_options()
            category = Category.objects.get(slug=self.slug_option)
        if form_product.is_valid():
            model_product = form_product.save()
            model_product.specification.clear()
            for key in request.POST.copy():
                if key.find('id_specification_') >= 0:
                    id_specification = key.replace('id_specification_', '')
                    value = int(request.POST.get(key)) if request.POST.get(key).isdigit() else None
                    id_specification = int(id_specification) if id_specification.isdigit() else None
                    if value and value != 0 and id_specification:
                        if ValuesOfSpecification.objects.filter(pk=value).exists() and Specification.objects.filter(
                                pk=id_specification).exists():
                            model_product.specification.add(ValuesOfSpecification.objects.get(pk=value))
                            model_product.save()
            if action == 'create':
                messages.add_message(request, messages.INFO, f'Продукт "{model_product.title}" успешно добавлен!')
                return 'redirect'
            elif action == 'change':
                messages.add_message(request, messages.INFO, f'Продукт "{model_product.title}" успешно изменен!')
                return 'redirect'
        specifications = []
        if action == 'create':
            specifications = Specification.objects.filter(category=category)
        if action == 'change':
            id_category = request.POST.get('category' or None)
            if id_category and id_category.isdigit() and Category.objects.filter(pk=id_category).exists():
                specifications = Specification.objects.filter(category=request.POST.get('category'))
        category_specification = []
        for specification in specifications:
            id_value_selected = request.POST.get(f'id_specification_{specification.pk}' or None)
            select = None
            if id_value_selected and id_value_selected.isdigit() and ValuesOfSpecification.objects.filter(pk=id_value_selected).exists():
                select = ValuesOfSpecification.objects.get(pk=id_value_selected).pk
            category_specification.append({
                'pk': specification.pk,
                'title': specification.title,
                'slug': specification.slug,
                'values': ValuesOfSpecification.objects.filter(specification=specification).values('pk', 'value'),
                'select': select
            })
        return category_specification


class PickupPointMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['points'] = PickUpPoints.objects.all()
        return context
