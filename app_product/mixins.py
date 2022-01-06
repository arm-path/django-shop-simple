from django.http import Http404
from app_profile.models import Customer

from .models import ValuesOfSpecification, CustomFilter, CartOrOrder


class FilterCategoryMixin:
    def get_product(self, get_request, product):
        custom_filter = False
        value_specification = []
        prefix_custom_filter = 'cm-filter-'
        value_of_specification_model = []
        for key in get_request.copy():
            if not key == 'page':
                values = get_request.getlist(key)
                if prefix_custom_filter in key:
                    if not key.startswith(prefix_custom_filter):
                        continue
                    key = key[len(prefix_custom_filter):]
                    custom_filter = True
                for value in values:
                    if not custom_filter and ValuesOfSpecification.objects.filter(specification__slug=key, value=value).exists():
                        value_specification.append(ValuesOfSpecification.objects.get(specification__slug=key, value=value))
                    if custom_filter and ValuesOfSpecification.objects.filter(specification__slug=key).exists():
                        if CustomFilter.objects.filter(pk=value).exists():
                            model_custom_filter = CustomFilter.objects.get(pk=value)
                            if model_custom_filter.lessOrEqual and model_custom_filter.moreOrEqual:
                                for specifiaction in ValuesOfSpecification.objects.filter(specification__slug=key):
                                    try:
                                        if model_custom_filter.moreOrEqual < int(specifiaction.value) < model_custom_filter.lessOrEqual:
                                            value_of_specification_model.append(specifiaction)
                                    except ValueError:
                                        continue
                            if model_custom_filter.lessOrEqual and not model_custom_filter.moreOrEqual:
                                for specifiaction in ValuesOfSpecification.objects.filter(specification__slug=key):
                                    try:
                                        if int(specifiaction.value) < model_custom_filter.lessOrEqual:
                                            value_of_specification_model.append(specifiaction)
                                    except ValueError:
                                        continue
                            if not model_custom_filter.lessOrEqual and model_custom_filter.moreOrEqual:
                                for specifiaction in ValuesOfSpecification.objects.filter(specification__slug=key):
                                    try:
                                        if model_custom_filter.moreOrEqual < int(specifiaction.value):
                                            value_of_specification_model.append(specifiaction)
                                    except ValueError:
                                        continue
                    if key == 'rating':
                        try:
                            product = product.filter(rating__gte=int(value))
                        except ValueError:
                            continue
                if value_of_specification_model:
                    for value_sp in value_of_specification_model:
                        value_specification.append(value_sp)
                product = product.filter(specification__in=value_specification).distinct()
                value_specification = []
        return product


class OrderCheckMixin:
    customer = None
    cart = None

    def order_check(self, user):
        self.customer = Customer.objects.filter(user=user).first()
        if not self.customer:
            raise Http404
        self.cart = CartOrOrder.objects.filter(customer=self.customer, is_cart=True).first()
        if not self.cart:
            raise Http404
        if not self.cart.products.all():
            raise Http404

    def form_check(self, order_form):
        if order_form.is_valid():
            self.cart.is_cart = False
            self.cart.save()
            order_model = order_form.save(commit=False)
            order_model.order = self.cart
            order_model.method_get = order_form.cleaned_data.get('method_get')
            order_model.pickup_point = order_form.cleaned_data.get('pickup_point')
            order_model.delivery_address = order_form.cleaned_data.get('delivery_address')
            order_model.method_payment = order_form.cleaned_data.get('method_payment')
            order_model.save()
            return redirect('detail_profile')
