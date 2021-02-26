from django.forms import ModelForm
from .models import Todo

class TodoForm(ModelForm): #inherit from django.forms
    class Meta:
        model = Todo #what model we want this to hold
        fields = ['title', 'memo', 'important'] #the fields we want to show up
