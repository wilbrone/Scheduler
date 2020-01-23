from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'image']


class NewEventForm(forms.ModelForm):
    
    date = forms.DateField(help_text='format, YY-mm-d')
    time = forms.TimeField(help_text='format, hr:min:sec')
    class Meta:
        model = Event
        fields = ['title','date','time']
        

    


    # title = models.CharField(max_length=100)
    # email = models.EmailField()
    # posted = models.DateTimeField(auto_now_add=True)
    # date = models.DateField()
    # time = models.TimeField()
    # color = models.CharField(max_length=10)
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
