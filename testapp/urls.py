from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [


    # Register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Login
    url(r'^login/$', views.login, name='login'),

    url('', include('django.contrib.auth.urls')),
]
