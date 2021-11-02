import json
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from .forms import CategoryForm, SpecificationForm
from .models import Category, Specification


class BaseView(View):
    """ Представление первоначальной страницы """

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})


class CategoryCreateView(CreateView):
    """ Представление создания Категории """
    model = Category
    form_class = CategoryForm
    template_name = 'app_product/category_create.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('category_change', args=(self.object.slug,))


class CategoryChangeView(View):
    """ Представление изменения категории """

    def get(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404()
        categories = Category.objects.all()
        model_category = Category.objects.get(slug=slug_category)
        specifications = Specification.objects.filter(category=model_category)
        form_category = CategoryForm(instance=model_category)
        form_specification = SpecificationForm()
        context = {
            'slug_categories': slug_category,
            'categories': categories,
            'specifications': specifications,
            'form_category': form_category,
            'form_specification': form_specification
        }
        return render(request, 'app_product/category_change.html', context=context)

    def post(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404()
        categories = Category.objects.all()
        model_category = Category.objects.get(slug=slug_category)
        specifications = Specification.objects.filter(category=model_category)
        form_category = CategoryForm(request.POST, instance=model_category)
        form_specification = SpecificationForm(request.POST or None)
        if form_category.is_valid():
            model_category = form_category.save()
            return redirect('category_change', slug=model_category.slug)

        context = {
            'slug_categories': slug_category,
            'categories': categories,
            'specifications': specifications,
            'form_category': form_category,
            'form_specification': form_specification
        }
        return render(request, 'app_product/category_change.html', context=context)


class SpecificationCreateView(View):
    """ Представление добавления Спецификации """

    def post(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404()

        client_data = json.loads(request.body.decode("utf-8"))
        form_data = {}
        if client_data['title'] and client_data['unit'] and client_data['use_filters'] and client_data['type_filter']:
            model_category = Category.objects.get(slug=slug_category)
            form_data['title'] = client_data['title']
            form_data['category'] = model_category
            form_data['unit'] = client_data['unit']
            form_data['use_filters'] = client_data['use_filters']
            form_data['type_filter'] = client_data['type_filter']

        form_specification = SpecificationForm(form_data)
        if form_specification.is_valid():
            return JsonResponse({'success': 'True'})
        else:
            print('Errors', form_specification.errors)
            errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form_specification.errors.items()]))
            return JsonResponse({'errors': json.dumps(form_specification.errors)})
