from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm #go ahead and create a form and pass it to the template
from django.contrib.auth.models import User

# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', { 'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            User.objects.create_user(request.POST['username'], password = request.POST['password1']) #dictionary to represent the values from the form

            #user = load above into this variable and then save it
            #user.save()

            #will show an error after submission because we didnt send back a response to the browser
        else:
            #Tell the user that the passwords do not match
            print('Didn\'t match')

