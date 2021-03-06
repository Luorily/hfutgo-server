from django.urls import path, include
from .apis import *
urlpatterns = [
    path('login', Login.as_view(), name='user_login'),
    path('is_login', Status.as_view(), name='user_is_login'),
    path('today', Today.as_view(), name='user_today'),
    path('new_user/', include('user.apis.new_user.urls'), name='new_user'),
    path('today_page/', include('user.apis.today.urls'), name='today_page'),
    path('forgot/', include('user.apis.forgot.urls'), name='user_forgot'),
    path('guest/', include('user.apis.guest.urls'), name='guest'),
    path('logout', Logout.as_view(), name='user_logout')
]
