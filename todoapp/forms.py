from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TaskModel


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', help_text='')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Again', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('taskTitle', 'taskDescription', 'taskDueDate', 'taskPriority')
        widgets = {
            'taskDueDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            }

class TaskFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    created_at = forms.DateField(required=False)
    due_date = forms.DateField(required=False)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=False)
    is_completed = forms.BooleanField(required=False, widget=forms.CheckboxInput)
