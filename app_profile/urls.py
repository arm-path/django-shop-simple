from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CreateProfileView, AuthenticationUserView, DetailProfileView, ChangeProfileView

urlpatterns = [
    path('create/', CreateProfileView.as_view(), name='registration'),
    path('authentication/', AuthenticationUserView.as_view(), name='authentication'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('view/', DetailProfileView.as_view(), name='detail_profile'),
    path('change/', ChangeProfileView.as_view(), name='change_profile')
]
