from __future__ import print_function
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

# google imports
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
import http.client

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .forms import *
from .models import *



SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secret.json')

# FLOW = flow_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope='https://www.googleapis.com/auth/calendar.readonly',
#     redirect_uri='http://www.notify-me.ua:8000/complete/google-oauth2/'
# )
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


    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    # service = build('calendar', 'v3', credentials=creds)

    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # event_result = service.events().list(calendarId="primary", timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # event = event_result.get('items', [])

    # if not event:
    #     print('No upcoming events found.')
    # for even in event:
    #     start = even['start'].get('dateTime', event['start'].get('date'))
    #     print(start, even['summary'])
# ***********************************************************************************************

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
