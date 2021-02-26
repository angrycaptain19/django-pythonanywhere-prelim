from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm #go ahead and create a form and pass it to the template

# Create your views here.

def signupuser(request):
    return render(request, 'todo/signupuser.html', { 'form': UserCreationForm()})
