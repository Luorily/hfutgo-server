from django.urls import path
from .Login import Login

urlpatterns = [
    path('login', Login.as_view(), name='guest_login'),
]