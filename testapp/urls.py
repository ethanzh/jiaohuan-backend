from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken import views as DRFviews

app_name = "testapp"

urlpatterns = [

    # Index
    url(r'^$', views.index, name='index'),


    # GET PK
    url(r'^current_user/', views.current_user, name='get_pk'),


    # Register
    url(r'^register/', csrf_exempt(views.UserFormView.as_view()), name='register'),

    # Phone Login
    url(r'^mobile_register/', csrf_exempt(views.MobileUserFormView.as_view()), name='mobile_register'),

    # Website Login
    url(r'^login/', auth_views.login,
        {'template_name': 'testapp/registration/login.html'}, name="login"),

    # Website Success
    url(r'^success/', views.success, name='success'),

    # Phone Success
    url(r'^mobile_login/success/', views.success, name="mobile_success"),

    # Displays list of user accounts, authentication needed
    url(r'^json/', views.UserList.as_view(), name='json'),

    # Helps obtain token when provided with username and password
    url(r'^api-token-auth/', DRFviews.obtain_auth_token),

    url(r'^profiles/home/', views.home),

    url(r'^auth/', views.AuthView.as_view(), name='auth-view'),


    # Update views

    # Update Company
    url(r'^update_company/', views.update_company, name='update_company'),

    # Update Phone
    url(r'^update_phone/', views.update_phone, name='update_phone'),

    # Update email
    url(r'^update_email/', views.update_email, name='update_email'),

    # Update location
    url(r'^update_location/', views.update_location, name='update_location'),

    # Update all
    url(r'^update/', views.update_user_info, name='update_user_info'),

    url(r'^friendship/', include('friendship.urls')),

    url(r'^add_friend/', views.friend_request, name='add_friend'),

    url(r'^friend_list/', views.get_friends_list, name='my_list_of_friends'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
