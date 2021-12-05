from django.contrib import admin
from .models import Customer


# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     """ Представление покупателя в административной панели """
#     list_display = ('user', )

admin.site.register(Customer)
