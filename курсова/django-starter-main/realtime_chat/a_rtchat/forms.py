from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Напишіть повідомлення ...', 'class': 'p-4 text-black', 'max_length' : '300', 'autofocus' : True}),
        }