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
    list_display = ('title', 'category', 'unit', 'type_filter')
    list_filter = ('category', 'type_filter')
    search_fields = ('title', )
    fields = ('title', 'category', 'unit', 'use_filters', 'type_filter')


admin.site.register(Product)
admin.site.register(ValuesOfSpecification)
admin.site.register(CustomFilterOne)
admin.site.register(CustomFilterTwo)
