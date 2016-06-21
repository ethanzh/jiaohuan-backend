from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from . forms import UserForm
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from . serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login,)
from django.contrib.auth.forms import (
    AuthenticationForm)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@csrf_exempt
def mobile_login(request, template_name='registration/login.html',
                 redirect_field_name=REDIRECT_FIELD_NAME,
                 authentication_form=AuthenticationForm,
                 extra_context=None):

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class UserList(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'Users': serializer.data})

    def post(self):
        pass


def success(request):
    return HttpResponse("<p> success! </p>")


def index(request):
    return render(request, 'testapp/index.html')


def login_user(request):
    return render(request, 'testapp/old_login.html')


class NonJSONUserList(generic.ListView):
    template_name = 'testapp/list_of_users.html'

    def get_queryset(self):
        return User.objects.all()


class UserFormView(View):
    form_class = UserForm
    template_name = 'testapp/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:

                    login(request, user)

                    return redirect('testapp:index')

        return render(request, self.template_name, {'form': form})
