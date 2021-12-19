from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """ Форма создания отзыва """

    class Meta:
        model = Review
        fields = ('customer', 'product', 'rating', 'review')
