from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from .models import TTUser, JobSeeker, Recruiter
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['email'],
                          password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def register(request):
    template_data = {}
    template_data['title'] = 'Register'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.onboard')
        else:
            template_data['form'] = form
            return render(request, 'accounts/register.html', {'template_data': template_data})
        
def onboard(request):
    template_data = {}
    return render(request, 'accounts/onboard.html', {'template_data': template_data})

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Accounts'
    return render(request, 'accounts/index.html', {'template_data': template_data})
# Create your views here.

def profiles(request, id):
    is_seeker = True
    user = TTUser.objects.get(id=id) 
    template_data = {}
    template_data['title'] = 'Profiles'
    template_data['user'] = user
    template_data['id'] = id
    print("other print")
    try:
        seeker_user = JobSeeker.objects.get(user_id=id)
        template_data["seeker_user"] = seeker_user
        template_data['education'] = seeker_user.education.all()
        #template_data['skills'] = seeker_user.education.all()
        template_data['experience'] = seeker_user.experience.all()
        #find some way to put links
        #find some way to put resume
        
    except Exception:
        is_seeker = False
        recruiter_user = Recruiter.objects.get(user_id=id)
        #something abt links
    template_data['is_seeker'] = is_seeker
    return render(request, 'accounts/profiles.html', {'template_data': template_data})