import random

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .forms import *
from .models import *

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup_form.html', {'form': form})


@login_required(login_url='login')
def index(request):
    events = Event.objects.all()
    current_user = request.user

    if request.method == 'POST':
        e_form = NewEventForm(request.POST, request.FILES)

        if e_form.is_valid():
            post = e_form.save(commit=False)
            post.user = request.user.profile
            post.email = request.user.email
            post.color = "%06x" % random.randint(0, 0xFFFFFF)
            post.save()
            return redirect ('index')
        
    else:
        e_form = NewEventForm(request.POST, request.FILES)

    context = {
        'e_form':e_form,
    }
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return render(request, 'all-reminders/index.html', locals())


@login_required(login_url='login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.all()

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=request.user)
        p_form = UpdateUserProfileForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            return render(request,'registration/profile.html')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateUserProfileForm(instance=request.user.profile)


    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'registration/profile.html',locals())


@login_required(login_url='login')
def single_event(request, id):
    return render(request, 'all-reminders/details.html' )