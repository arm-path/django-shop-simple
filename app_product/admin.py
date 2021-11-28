from django.contrib import admin

from .models import Category, Product, Specification, ValuesOfSpecification, CustomFilter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Представление категории в административной панели """
    list_display = ('title', 'slug')
    fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Представление продуктов в административной панели """
    list_display = ('title', 'category', 'price', 'rating')
    list_filter = ('category__title',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'category', 'image', 'price', 'product_availability', 'description', 'specification')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """ Представление характеристик в административной панели """
    list_display = ('title', 'slug', 'category', 'unit', 'type_filter')
    list_filter = ('category', 'type_filter')
    search_fields = ('title',)
    fields = ('title', 'category', 'unit', 'use_filters', 'type_filter')


@admin.register(ValuesOfSpecification)
class ValuesOfSpecificationAdmin(admin.ModelAdmin):
    """ Представление значений характеристик в административной панели """
    list_display = ('specification', 'value', 'get_unit')
    list_filter = ('specification__title',)
    fields = ('specification', 'value')

    def get_unit(self, obj):
        return obj.specification.unit

    get_unit.short_description = 'Ед. измерения'


@admin.register(CustomFilter)
class CustomFilterAdmin(admin.ModelAdmin):
    """ Представление кастомных фильтров №1 в административной панели """
    list_display = ('specification', 'lessOrEqual', 'moreOrEqual')
    list_filter = ('specification__title',)
