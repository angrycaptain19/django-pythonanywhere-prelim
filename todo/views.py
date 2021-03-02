from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', { 'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(
                    request,
                    'todo/signupuser.html',
                    {
                        'form':UserCreationForm(),
                        'error':'That username has already been taken. Please choose a new username'
                    }
                )
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', { 'form': AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password are incorrect'})
    login(request, user)
    return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        # pass
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False) #create a new form object but dont save to database yet
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

#do this first
# def currenttodos(request):
#     todos = Todo.objects.all()
#     return render(request, 'todo/currenttodos.html', {'todos': todos })

#do this to show only your own todos
# def currenttodos(request):
#     todos = Todo.objects.filter(user=request.user)
#     return render(request, 'todo/currenttodos.html', {'todos': todos })

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) #special naming convention by django model
    return render(request, 'todo/currenttodos.html', {'todos': todos })

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos })

# def viewtodo(request, todo_pk):
#     todo = get_object_or_404(Todo, pk=todo_pk)
#     return render(request, 'todo/viewtodo.html', {'todo': todo})
# def viewtodo(request, todo_pk):
#     todo = get_object_or_404(Todo, pk=todo_pk)
#     form = TodoForm(instance=todo)
#     return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form })

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #addthe user later to show we shouldnt update other users todo
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form })
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'error':'Bad information' })

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

def handler404(request,exception):
	return render(request,'todo/404.html', status=404)
def handler500(request, *args, **argv):
    return render(request, 'todo/500.html', status=500)
