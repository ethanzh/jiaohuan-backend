from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from . forms import UserForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from . serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,)
from django.contrib.auth.forms import (AuthenticationForm)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AuthView(APIView):
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({'detail': "I suppose you are authenticated"})


@login_required
def home(request):
    return HttpResponseRedirect(reverse(profile(request), args=[request.user.username]))


def profile(request, user):
    return render(request, 'testapp/profile.html', {"variable": user})


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def success(request):
    return HttpResponse("<p> Success! </p>")


def index(request):
    return render(request, 'testapp/index.html')


class UserFormView(View):

    form_class = UserForm
    template_name = 'testapp/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    @csrf_exempt
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


class MobileUserFormView(View):

    form_class = UserForm
    template_name = 'testapp/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return HttpResponse(200)

    @csrf_exempt
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

                    return HttpResponse(200)

        return HttpResponse("Not found")
