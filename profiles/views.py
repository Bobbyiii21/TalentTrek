from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'profiles/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'],
                          password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'profiles/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def register(request):
    template_data = {}
    template_data['title'] = 'Register'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'profiles/register.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('profiles.onboard')
        else:
            template_data['form'] = form
            return render(request, 'profiles/register.html', {'template_data': template_data})
        
def onboard(request):
    template_data = {}
    return render(request, 'profiles/onboard.html', {'template_data': template_data})

from django.shortcuts import render
# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Profiles'
    return render(request, 'profiles/index.html', {'template_data': template_data})
# Create your views here.

