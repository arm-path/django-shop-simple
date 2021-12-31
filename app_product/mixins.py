from django.http import Http404
from app_profile.models import Customer

from .models import ValuesOfSpecification, CustomFilter, CartOrOrder


class FilterCategoryMixin:
    def get_product(self, GET_REQUEST, product):
        custom_filter = False
        value_specification = []
        prefix_custom_filter = 'cm-filter-'
        value_of_specification_model = None
        for key in GET_REQUEST.copy():
            values = GET_REQUEST.getlist(key)
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
                            value_of_specification_model = ValuesOfSpecification.objects.filter(
                                specification__slug=key, value__lte=model_custom_filter.lessOrEqual,
                                value__gte=model_custom_filter.moreOrEqual)
                        if model_custom_filter.lessOrEqual and not model_custom_filter.moreOrEqual:
                            value_of_specification_model = ValuesOfSpecification.objects.filter(
                                specification__slug=key, value__lte=model_custom_filter.lessOrEqual)
                        if not model_custom_filter.lessOrEqual and model_custom_filter.moreOrEqual:
                            value_of_specification_model = ValuesOfSpecification.objects.filter(
                                specification__slug=key, value__gte=model_custom_filter.moreOrEqual)
            if value_of_specification_model:
                for value_sp in value_of_specification_model:
                    value_specification.append(value_sp)
            product = product.filter(specification__in=value_specification).distinct()
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
