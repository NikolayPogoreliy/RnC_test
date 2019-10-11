from django.urls import path

from apps.account.views import login_view


urlpatterns = [
    path('', login_view, name='base_login')
]