from django import forms
from .models import TaskModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('taskTitle', 'taskDescription', 'taskDueDate', 'taskPriority')


class TaskFilterForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    created_at = forms.DateField(required=False)
    due_date = forms.DateField(required=False)
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=False)
    is_completed = forms.BooleanField(required=False, widget=forms.CheckboxInput)
