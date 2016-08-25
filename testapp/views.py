from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from . forms import UserForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from . serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import simplejson
from rest_framework.decorators import api_view
from friendship.models import Friend
from friendship.models import FriendshipRequest
from django.core import serializers


@csrf_exempt
def get_user_and_friends_list(request):
    print(request.user.username)

    json = {
        "Username": request.user.username
    }
    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')


@api_view(['GET'])
def current_user(request):
    #serializer = UserSerializer(request.user)

    my_user = request.user

    my_serialized_user = serializers.serialize('json', my_user)


    json = {
        my_serialized_user
    }

    data = simplejson.dumps(json)

    #return Response(serializer.data)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_friends_list(request):

    my_pk = int(request.POST['my_pk'])
    my_user = User.objects.get(pk=my_pk)

    all_friends = Friend.objects.friends(my_user)
    ser_friend = serializers.serialize('json', all_friends)

    print(my_pk)
    print(all_friends)

    return HttpResponse(ser_friend, content_type='application/json')


@csrf_exempt
def friend_request(request):

    my_pk = int(request.POST['my_pk'])
    their_pk = int(request.POST['their_pk'])

    my_user = User.objects.get(pk=my_pk)
    their_user = User.objects.get(pk=their_pk)

    adding_to_database = Friend.objects.add_friend(
        my_user,
        their_user,
    )

    adding_to_database.save()

    id_number = adding_to_database.pk

    db_request = FriendshipRequest.objects.get(pk=id_number)
    db_request.accept()

    my_name = my_user.get_username()
    their_name = their_user.get_username()

    json = {

        "My Name": my_name,
        "Their Name": their_name,
        "id": id_number
    }

    data = simplejson.dumps(json)

    print("My name: " + my_name + "\nTheir Name: " + their_name)

    return HttpResponse(data, content_type='application/json')


class AuthView(APIView):
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    if IsAuthenticated:
        print("Authenticated!")
    else:
        print("Not Authenticated!")

    def get(self, request, format=None):
        return Response({'detail': "I suppose you are authenticated",})


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

        error = form.errors;
        form_error = form.non_field_errors();

        error_json = {

            "form": error,
            "form_error": form_error

        }

        error_data = simplejson.dumps(error_json)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user_json = {

                "Authenticated": True,

                "Username": username,


            }

            data = simplejson.dumps(user_json)

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:

                    login(request, user)

                    return HttpResponse(data, content_type='application/json')

        return HttpResponse(error_data, content_type='application/json')


@csrf_exempt
def update_company(request):

    final = request.POST['company']

    id_number = request.POST['id_number']

    user_details = User.objects.get(pk=id_number)
    user_details.company = final
    user_details.save()

    json = {

        "Company": final,
        "id": id_number
    }

    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def update_email(request):

    final = request.POST['email']

    id_number = request.POST['id_number']

    user_details = User.objects.get(pk=id_number)
    user_details.email = final
    user_details.save()

    json = {

        "Email": final,
        "id": id_number
    }

    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def update_phone(request):

    final = request.POST['phone_number']

    id_number = request.POST['id_number']

    user_details = User.objects.get(pk=id_number)
    user_details.phone_number = final
    user_details.save()

    json = {

        "Phone Number": final,
        "id": id_number
    }

    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def update_location(request):

    final = request.POST['location']

    id_number = request.POST['id_number']

    user_details = User.objects.get(pk=id_number)
    user_details.location = final
    user_details.save()

    json = {

        "Location": final,
        "id": id_number
    }

    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def update_user_info(request):

    id_number = request.POST['id_number']
    request_email = request.POST['email']
    request_phone_number = request.POST['phone_number']
    request_location = request.POST['location']
    request_company = request.POST['company']

    user_detail = User.objects.get(pk=id_number)

    print("\nFields:")

    if request_email == "":
        print("Email = False")
    elif request_email != "":
        print("Email = True")
        user_detail.email = request_email

    if request_phone_number == "":
        print("Phone number = False")
    elif request_phone_number != "":
        print("Phone number = True")
        user_detail.phone_number = request_phone_number

    if request_location == "":
        print("Location = False")
    elif request_location != "":
        print("Location = True")
        user_detail.location = request_location

    if request_company == "":
        print("Company = False")

    elif request_company != "":
        print("Company = True")
        user_detail.company = request_company

    user_detail.save()

    json = {
        "ID": id_number,
        "Email": request_email,
        "Phone Number": request_phone_number,
        "Location": request_location,
        "Company": request_company
    }

    data = simplejson.dumps(json)

    return HttpResponse(data, content_type='application/json')