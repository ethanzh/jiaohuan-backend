from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from django.contrib.auth import views as auth_views

app_name = "testapp"

urlpatterns = [

    # Index
    url(r'$', views.index, name='index'),

    # List
    url(r'^list/$', views.UserList.as_view(), name='list'),

    # Register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Login
    url(r'^login/$', auth_views.login,
        {'template_name': 'testapp/registration/login.html'}, name="login"),

    # Success
    url(r'^success/$', views.success, name='success'),

]
