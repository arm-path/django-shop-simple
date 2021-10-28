from django.contrib import admin

from .models import Category, Product, Specification, ValuesOfSpecification, CustomFilterOne, CustomFilterTwo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Представление категории в административной панели """
    list_display = ('title', 'slug')
    fields = ('title',)


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """ Представление характеристик в административной панели """
    list_display = ('title', 'slug', 'category', 'unit', 'type_filter')
    list_filter = ('category', 'type_filter')
    search_fields = ('title', )
    fields = ('title', 'category', 'unit', 'use_filters', 'type_filter')


@admin.register(ValuesOfSpecification)
class ValuesOfSpecificationAdmin(admin.ModelAdmin):
    """ Представление значений характеристик в административной панели """
    list_display = ('specification', 'value', 'get_unit')
    list_filter = ('specification__title',)
    fields = ('specification', 'value', 'products')

    def get_unit(self, obj):
        return obj.specification.unit
    
    get_unit.short_description = 'Ед. измерения'


@admin.register(CustomFilterOne)
class CustomFilterOneAdmin(admin.ModelAdmin):
    """ Представление кастомных фильтров №1 в административной панели """
    list_display = ('specification', 'lessOrEqual', 'moreOrEqual')
    list_filter = ('specification__title',)


@admin.register(CustomFilterTwo)
class CustomFilterTwoAdmin(admin.ModelAdmin):
    """ Представление кастомных фильтров №2 в административной панели """
    list_display = ('specification', 'get_filter_name')
    list_filter = ('specification__title',)


    def get_filter_name(self, obj):
        return f'от {str(obj.from_digit)} до {str(obj.before_digit)}'
    
    get_filter_name.short_description = 'Фильтр'



admin.site.register(Product)

