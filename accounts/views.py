from django.shortcuts import get_object_or_404, render
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
    user = TTUser.objects.get(id=id) 
    template_data = {}
    template_data['title'] = 'Profiles'
    template_data['user'] = user
    template_data['id'] = id
    template_data['is_seeker'] = True
    try:
        seeker_user = JobSeeker.objects.get(user_id=id)
        template_data["seeker_user"] = seeker_user
        template_data['education'] = seeker_user.education.all()
        #template_data['skills'] = seeker_user.education.all()
        template_data['experience'] = seeker_user.experience.all()
        template_data['links'] = seeker_user.links.split(",")
        for link in template_data['links']:
            link = link.strip()
        #find some way to put resume
        
    except Exception:
        template_data['is_seeker'] = False
        recruiter_user = Recruiter.objects.get(user_id=id)
        template_data['recruiter_user'] = recruiter_user
        template_data['links'] = recruiter_user.links.split(",")
        for link in template_data['links']:
            link = link.strip()
    return render(request, 'accounts/profiles.html', {'template_data': template_data})

@login_required
def edit_profile(request, id):
    profile = get_object_or_404(TTUser, id)
    if request.user != profile.user:
        return redirect('accounts.profiles')
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = "Edit Profile"
        template_data['profile'] = profile
        template_data['is_seeker'] = True
        try:
            template_data['seeker_user'] = JobSeeker.objects.get(user_id=id)
        except Exception:
            template_data['recruiter_user'] = Recruiter.objects.get(user_id=id)
            template_data['is_seeker'] = False
        return render(request, 'accounts/edit_profile.html', {'template_data': template_data})
    elif request.method == 'POST':
        profile = TTUser.objects.get(id=id)
        profile.save()
        try:
            seeker_user = JobSeeker.objects.get(user_id=id)
            seeker_user.save()
        except:
            recruiter_user = Recruiter.objects.get(user_id=id)
            recruiter_user.save()
        return redirect('accounts.profiles')
    else:
        return redirect('accounts.profiles')
