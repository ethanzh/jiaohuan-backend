from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = "testapp"

urlpatterns = [

    # Index
    url(r'^index/$', views.index, name='index'),

    # List
    url(r'^list/$', views.UserList.as_view(), name='list'),

    # Register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url('', include('django.contrib.auth.urls')),
]
