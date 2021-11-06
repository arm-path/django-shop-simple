import json
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DeleteView
from django.forms.models import model_to_dict

from .forms import CategoryForm, SpecificationForm, ValuesOfSpecificationForm
from app_product.models import Category, Specification, ValuesOfSpecification


class CategoryCreateView(CreateView):
    """ Представление создания категории """
    model = Category
    form_class = CategoryForm
    template_name = 'app_control/category_create.html'

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
            'slug_category': slug_category, 'categories': categories, 'specifications': specifications,
            'form_category': form_category, 'form_specification': form_specification
        }
        return render(request, 'app_control/category_change.html', context=context)

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
            'slug_category': slug_category, 'categories': categories, 'specifications': specifications,
            'form_category': form_category, 'form_specification': form_specification
        }
        return render(request, 'app_control/category_change.html', context=context)


class SpecificationCreateView(View):
    """ Представление добавления характеристики """

    def post(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404()

        client_data = json.loads(request.body.decode("utf-8"))
        form_data = {}
        if client_data['title'] and client_data['type_filter']:
            form_data = {
                'title': client_data['title'], 'category': Category.objects.get(slug=self.kwargs.get('slug')).pk,
                'unit': client_data['unit'], 'use_filters': client_data['use_filters'], 'type_filter': client_data['type_filter']
            }
        form_specification = SpecificationForm(form_data)
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        else:
            return JsonResponse({'errors': form_specification.errors})


class SpecificationChangeView(View):
    """ Представление изменения характеристики """

    def get(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        id_specification = self.kwargs.get('pk')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404
        if not Specification.objects.filter(id=id_specification).exists():
            raise Http404
        return JsonResponse({'specification': model_to_dict(Specification.objects.get(id=id_specification))})

    def post(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        id_specification = self.kwargs.get('pk')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404
        if not Specification.objects.filter(id=id_specification).exists():
            raise Http404

        client_data = json.loads(request.body.decode('utf-8'))
        form_data = {}
        if client_data['title'] and client_data['type_filter']:
            form_data = {
                'title': client_data['title'], 'category': Category.objects.get(slug=self.kwargs.get('slug')).pk,
                'unit': client_data['unit'], 'use_filters': client_data['use_filters'], 'type_filter': client_data['type_filter']
            }
        form_specification = SpecificationForm(form_data, instance=Specification.objects.get(id=id_specification))
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        return JsonResponse({'errors': form_specification.errors})


class SpecificationDeleteView(View):
    """ Представление удаления характеристики """

    def get(self, request, *args, **kwargs):
        slug_category = self.kwargs.get('slug')
        id_specification = self.kwargs.get('pk')
        if not Category.objects.filter(slug=slug_category).exists():
            raise Http404
        if not Specification.objects.filter(id=id_specification).exists():
            raise Http404
        Specification.objects.get(id=id_specification).delete()
        return redirect('category_change', slug=slug_category)


class ValuesOfSpecificationCreateView(View):
    """ Представление Добавления Значения Характеристики """

    def get(self, request, *args, **kwargs):
        slug_specification = self.kwargs.get('slug')
        if not Specification.objects.filter(slug=slug_specification).exists():
            raise Http404

        categories = Category.objects.all()
        values_specification = ValuesOfSpecification.objects.filter(specification__slug=slug_specification)

        form_value_specification = ValuesOfSpecificationForm()
        context = {
            'slug_specification': self.kwargs.get('slug'), 'form_value_specification': form_value_specification,
            'categories': categories, 'values_specification': values_specification,
            'specification': Specification.objects.get(slug=slug_specification)
        }
        return render(request, 'app_control/specification_change.html', context)

    def post(self, request, *args, **kwargs):
        slug_specification = self.kwargs.get('slug')
        if not Specification.objects.filter(slug=slug_specification).exists():
            raise Http404

        client_data = json.loads(request.body.decode('utf-8'))
        form_data = {'specification': Specification.objects.get(slug=slug_specification).pk, 'value': client_data['value']}

        form_value_specification = ValuesOfSpecificationForm(form_data)
        if form_value_specification.is_valid():
            form_value_specification.save()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse({'errors': form_value_specification.errors})


class ValueOfSpecificationChangeView(View):
    """ Представление изменения значения характеристики """

    def get(self, request, *args, **kwargs):
        slug_specification = self.kwargs.get('slug')
        id_value_specification = self.kwargs.get('pk')
        if not Specification.objects.filter(slug=slug_specification).exists():
            raise Http404
        if not ValuesOfSpecification.objects.filter(id=id_value_specification).exists():
            raise Http404
        return JsonResponse({'value_specification': model_to_dict(ValuesOfSpecification.objects.get(id=id_value_specification))})

    def post(self, request, *args, **kwargs):
        slug_specification = self.kwargs.get('slug')
        id_value_specification = self.kwargs.get('pk')
        if not Specification.objects.filter(slug=slug_specification).exists():
            raise Http404
        if not ValuesOfSpecification.objects.filter(id=id_value_specification).exists():
            raise Http404

        client_data = json.loads(request.body.decode('utf-8'))
        if client_data['value']:
            form_data = {'specification': Specification.objects.get(slug=slug_specification).pk, 'value': client_data['value']}
        form_specification = ValuesOfSpecificationForm(form_data, instance=ValuesOfSpecification.objects.get(id=id_value_specification))
        if form_specification.is_valid():
            form_specification.save()
            return JsonResponse({'success': 'True'})
        return JsonResponse({'errors': form_specification.errors})


class ValueSpecificationDeleteView(View):
    """ Представление удаления значения харкатеристики """

    def get(self, request, *args, **kwargs):
        slug_specification = self.kwargs.get('slug')
        id_value_specification = self.kwargs.get('pk')
        if not Specification.objects.filter(slug=slug_specification).exists():
            raise Http404
        if not ValuesOfSpecification.objects.filter(id=id_value_specification).exists():
            raise Http404

        ValuesOfSpecification.objects.get(id=id_value_specification).delete()
        return redirect('specification_value', slug=slug_specification)
