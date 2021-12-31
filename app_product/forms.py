from django import forms
from django.core.exceptions import ValidationError

from .models import Review, Order


class ReviewForm(forms.ModelForm):
    """ Форма создания отзыва """

    class Meta:
        model = Review
        fields = ('customer', 'product', 'rating', 'review')


class OrderForm(forms.ModelForm):
    """ Форма оформления заказа """

    def clean(self):
        cleaned_data = super().clean()
        method_get = cleaned_data.get('method_get')
        pickup_point = cleaned_data.get('pickup_point')
        delivery_address = cleaned_data.get('delivery_address')

        if method_get == Order.PICKUP and not pickup_point:
            self.add_error('pickup_point', 'Заполните адресс самовывоза!')
        if method_get == Order.DELIVERY and not delivery_address:
            self.add_error('delivery_address', 'Заполните адрес доставки')

    class Meta:
        model = Order
        fields = ('method_get', 'pickup_point', 'delivery_address', 'method_payment')
        widgets = {
            'method_get': forms.Select(attrs={'class': 'form-control mb-2'}),
            'pickup_point': forms.Select(attrs={'class': 'form-control mb-2'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'method_payment': forms.Select(attrs={'class': 'form-control mb-2'})
        }
