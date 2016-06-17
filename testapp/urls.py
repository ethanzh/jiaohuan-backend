from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^', views.test, name='test'),

    url(r'^register$', views.UserFormView.as_view(), name='register'),
]
