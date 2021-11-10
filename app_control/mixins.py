from django.http import Http404

from app_product.models import Category, Specification, ValuesOfSpecification
from .forms import SpecificationForm, ValuesOfSpecificationForm


class BaseMixin:
    def check_options(self, slug_model='Category', id_model='Specification'):
        self.slug_option = self.kwargs.get('slug')
        self.id_option = self.kwargs.get('pk')
        if self.slug_option:
            if slug_model == 'Category' and not Category.objects.filter(slug=self.slug_option).exists():
                raise Http404()
            if slug_model == 'Specification' and not Specification.objects.filter(slug=self.slug_option).exists():
                raise Http404()
        if self.id_option:
            if id_model == 'Specification' and not Specification.objects.filter(id=self.id_option).exists():
                raise Http404
            if id_model == 'ValueSpecification' and not ValuesOfSpecification.objects.filter(id=self.id_option).exists():
                raise Http404


class CategoryChangeMixin(BaseMixin):
    def get_context(self):
        self.check_options()
        categories = Category.objects.all()
        self.model_category = Category.objects.get(slug=self.slug_option)
        specifications = Specification.objects.filter(category=self.model_category)
        form_specification = SpecificationForm()
        context = {
            'slug_category': self.slug_option,
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


class CreateProductMixin(BaseMixin):
    def get_context(self):
        self.check_options()
        form_value_specification = ValuesOfSpecificationForm()
        self.category = Category.objects.get(slug=self.slug_option)
        self.specifications = Specification.objects.filter(category=self.category)
        category_specification = []
        for specification in self.specifications:
            category_specification.append({
                'pk': specification.pk,
                'title': specification.title,
                'slug': specification.slug,
                'values': ValuesOfSpecification.objects.filter(specification=specification).values('pk', 'value'),
            })
        context = {
            'category': self.category,
            'form_value_specification': form_value_specification,
            'category_specification': category_specification
        }
        return context


