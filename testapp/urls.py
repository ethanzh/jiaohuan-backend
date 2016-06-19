from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

app_name = "testapp"

urlpatterns = [

    # Index
    url(r'^index/$', views.index, name='index'),

    # Login
    # url(r'^login/$', views.login_user, name='login'),

    # List
    url(r'^list/$', views.UserList.as_view(), name='list'),

    # Register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # url(
    #     regex=r'^login/$',
    #     view=login,
    #     kwargs={'template_name': 'login.html'},
    #     name='login'
    # ),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'testapp/registration/login.html'}, name="login"),

]
