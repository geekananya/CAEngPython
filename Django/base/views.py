from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Course
from .forms import CourseForm

# auth
def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('menu')
            else:
                messages.error(request, 'Invalid Credentials')
        except:
            messages.error(request, 'User does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'An error occurred!')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


# CRUD

@login_required(login_url ='/')
def menu(request):
    return render(request, 'base/home.html')


@login_required(login_url ='/')
def get_courses (request):
    courses = Course.objects.all()
    for c in courses:
        # print(type(c))
        print(c)
    context = {"courses": courses}
    return render(request, 'base/view.html', context)


@login_required(login_url ='/')
def get_course (request, pk):
    course = Course.objects.get(id = pk)
    context = {"course": course}
    return render(request, 'base/view_course.html', context)


@login_required(login_url ='/')
def add_course(request):
    form = CourseForm
    if request.method == 'POST' :
        form = CourseForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('menu')
    context = {"form": form}
    return render(request, 'base/course_form.html', context)

@login_required(login_url ='/')
def update_course(request, pk):
    course = Course.objects.get(id = pk)
    form = CourseForm(instance = course)
    if request.method == 'POST' :
        form = CourseForm(request.POST, instance=course)
        if form.is_valid() :
            form.save()
            return redirect('menu')
    context = {"form": form}
    return render(request, 'base/course_form.html', context)

@login_required(login_url ='/')
def delete_course(request, pk):
    course = Course.objects.get(id = pk)
    if request.method == 'POST' :
        course.delete()
        return redirect('menu')
    return render(request, 'base/delete.html', {"obj": course})


