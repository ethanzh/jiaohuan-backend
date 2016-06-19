from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "testapp"

urlpatterns = [

    # Index
    url(r'index/$', views.index, name='index'),

    # List
    url(r'^list/$', views.NonJSONUserList.as_view(), name='list'),

    # Register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Login
    url(r'^login/$', auth_views.login,
        {'template_name': 'testapp/registration/login.html'}, name="login"),

    # Success
    url(r'^success/$', views.success, name='success'),


    # JSON Data
    url(r'^json/$', views.UserList.as_view(), name='json'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
