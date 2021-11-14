import json

from django.forms.models import model_to_dict
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from app_product.models import Category, Specification, ValuesOfSpecification, Product
from .forms import (CategoryForm,
                    SpecificationForm,
                    ValuesOfSpecificationForm,
                    ProductForm, ProductAdditionallyForm)
from .mixins import (BaseMixin,
                     CategoryChangeMixin,
                     SpecificationCreateAndChangeMixin,
                     ValuesOfSpecificationCreateAndChangeMixin,
                     CreateAndChangeProductMixin)


class CategoryCreateView(CreateView):
    """ Представление добавления категории """
    model = Category
    form_class = CategoryForm
    template_name = 'app_control/category_create.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('category_change', args=(self.object.slug,))


class CategoryChangeView(CategoryChangeMixin, View):
    """ Представление изменения категории """

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        form_category = CategoryForm(instance=self.model_category)
        context['form_category'] = form_category
        return render(request, 'app_control/category_change.html', context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()
        form_category = CategoryForm(request.POST, instance=self.model_category)
        if form_category.is_valid():
            model_category = form_category.save()
            return redirect('category_change', slug=model_category.slug)
        context['form_category'] = form_category
        return render(request, 'app_control/category_change.html', context=context)


class SpecificationCreateView(SpecificationCreateAndChangeMixin, View):
    """ Представление добавления характеристики """

    def post(self, request, *args, **kwargs):
        form_data = self.get_form_data(json.loads(request.body.decode('utf-8')))
        form_specification = SpecificationForm(form_data)
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        else:
            return JsonResponse({'errors': form_specification.errors})


class SpecificationChangeView(SpecificationCreateAndChangeMixin, View):
    """ Представление изменения характеристики """

    def get(self, request, *args, **kwargs):
        self.check_options()
        return JsonResponse({'specification': model_to_dict(Specification.objects.get(id=self.id_option))})

    def post(self, request, *args, **kwargs):
        form_data = self.get_form_data(json.loads(request.body.decode('utf-8')))
        form_specification = SpecificationForm(form_data, instance=Specification.objects.get(id=self.id_option))
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        return JsonResponse({'errors': form_specification.errors})


class SpecificationDeleteView(BaseMixin, View):
    """ Представление удаления характеристики """

    def get(self, request, *args, **kwargs):
        self.check_options()
        Specification.objects.get(id=self.id_option).delete()
        return redirect('category_change', slug=self.slug_option)


class ValuesOfSpecificationCreateView(ValuesOfSpecificationCreateAndChangeMixin, View):
    """ Представление Добавления Значения Характеристики """

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, 'app_control/specification_change.html', context)

    def post(self, request, *args, **kwargs):
        form_data = self.get_form_data(json.loads(request.body.decode('utf-8')))
        form_value_specification = ValuesOfSpecificationForm(form_data)
        if form_value_specification.is_valid():
            value_specification = form_value_specification.save()
            return JsonResponse({'success': model_to_dict(value_specification)})
        else:
            return JsonResponse({'errors': form_value_specification.errors})


class ValueOfSpecificationChangeView(ValuesOfSpecificationCreateAndChangeMixin, View):
    """ Представление изменения значения характеристики """

    def get(self, request, *args, **kwargs):
        self.check_options(slug_model='Specification', id_model='ValueSpecification')
        return JsonResponse({'value_specification': model_to_dict(ValuesOfSpecification.objects.get(id=self.id_option))})

    def post(self, request, *args, **kwargs):
        form_data = self.get_form_data(json.loads(request.body.decode('utf-8')))
        form_specification = ValuesOfSpecificationForm(form_data, instance=ValuesOfSpecification.objects.get(id=self.id_option))
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        return JsonResponse({'errors': form_specification.errors})


class ValueSpecificationDeleteView(BaseMixin, View):
    """ Представление удаления значения харкатеристики """

    def get(self, request, *args, **kwargs):
        self.check_options(slug_model='Specification', id_model='ValueSpecification')
        ValuesOfSpecification.objects.get(id=self.id_option).delete()
        return redirect('specification_value_create', slug=self.slug_option)


class ControlProductView(View):
    """ Представление выбора категории для добавления продукта """

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'app_control/product_control.html', {'categories': categories})

    def post(self, request, *args, **kwargs):
        categories = Category.objects.all()
        if request.POST.get('category'):
            if Category.objects.filter(slug=request.POST.get('category')).exists():
                return redirect('product_create', slug=request.POST.get('category'))
            else:
                raise Http404
        return render(request, 'app_control/product_control.html', {'categories': categories})


class CreateProductView(CreateAndChangeProductMixin, View):
    """ Представление добавления продукта """

    def get(self, request, *args, **kwargs):
        context = self.get_context(slug_model='Category')
        context['form_product'] = ProductForm()
        return render(request, 'app_control/product_create.html', context)

    def post(self, request, *args, **kwargs):
        self.check_options()
        category = Category.objects.get(slug=self.slug_option)
        form_data = request.POST.copy()
        form_data.__setitem__('category', str(category.pk))
        form_product = ProductForm(form_data, files=request.FILES or None)
        category_specification = self.get_post_general(request=request, action='create', form_product=form_product)
        if category_specification == 'redirect':
            return redirect('product_create_control')
        context = {
            'category': category,
            'form_product': form_product,
            'form_value_specification': ValuesOfSpecificationForm(),
            'category_specification': category_specification
        }
        return render(request, 'app_control/product_create.html', context)


class ChangeProductView(CreateAndChangeProductMixin, View):
    """ Представление изменения продукта """

    def get(self, request, *args, **kwargs):
        context = self.get_context(slug_model='Product')
        context['form_product'] = ProductAdditionallyForm(instance=self.model_product)
        return render(request, 'app_control/product_change.html', context)

    def post(self, request, *args, **kwargs):
        self.check_options(slug_model='Product')
        model_product = Product.objects.get(slug=self.slug_option)
        form_product = ProductForm(request.POST, instance=model_product or None)
        category_specification = self.get_post_general(request=request, action='change', form_product=form_product)
        if category_specification == 'redirect':
            return redirect('product_change', slug=model_product.slug)
        context = {
            'form_product': form_product,
            'category_specification': category_specification,
            'form_value_specification': ValuesOfSpecificationForm(),
            'slug_product': self.slug_option
        }
        return render(request, 'app_control/product_change.html', context)


class ChangeCategoryInProductView(View):
    """ Представление изменения категории в прдставлении изменения продукта """

    def get(self, request, *args, **kwargs):
        slug_product = self.kwargs.get('slug')
        id_category = self.kwargs.get('pk')
        model_category = Category.objects.get(pk=id_category)
        category_specification = []
        specifications = Specification.objects.filter(category=model_category)
        for specification in specifications:
            category_specification.append({
                'pk': specification.pk,
                'title': specification.title,
                'slug': specification.slug,
                'values': list(ValuesOfSpecification.objects.filter(specification=specification).values('pk', 'value'))
            })
        print(category_specification)
        return JsonResponse({'category_specification': category_specification})
