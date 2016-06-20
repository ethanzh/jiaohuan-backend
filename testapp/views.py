from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from . forms import UserForm
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from rest_framework.views import APIView
from . serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
