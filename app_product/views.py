from django.shortcuts import render
from django.views import View


class BaseView(View):
    """ Представление первоначальной страницы """

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'base.html', {})
