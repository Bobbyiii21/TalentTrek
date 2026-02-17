from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import JobSeeker, Recruiter, DegreeType

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request, just_registered=False):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif just_registered:
        user = authenticate(request, username = request.POST['email'],
                          password = request.POST['password1'])
        auth_login(request, user)
        return
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
            login(request, just_registered=True)
            return redirect('accounts.onboard')
        else:
            template_data['form'] = form
            return render(request, 'accounts/register.html', {'template_data': template_data})

@login_required    
def onboard(request):
    if request.method == 'POST':
        print('ONBARD POST')
        if (request.POST['user_type'] == 'job_seeker'):
            job_seeker = JobSeeker()
            job_seeker.user = request.user
            if (request.POST['headline'] and request.POST['headline'].strip()):
                request.user.headline = request.POST['headline'].strip()
            if ('pfp' in request.FILES):
                request.user.pfp = request.FILES['pfp']
            if ('resume' in request.FILES):
                job_seeker.resume = request.FILES['resume']
            if (request.POST['links'] and request.POST['links'].strip()):
                job_seeker.links = request.POST['links'].strip()
            request.user.save()
            job_seeker.save()
        else:
            recruiter = Recruiter()
            recruiter.user = request.user
            if (request.POST['headline'] and request.POST['headline'].strip()):
                request.user.headline = request.POST['headline'].strip()
            if ('pfp' in request.FILES):
                request.user.pfp = request.FILES['pfp']
            if (request.POST['company'] and request.POST['company'].strip()):
                recruiter.company = request.POST['company'].strip()
            if (request.POST['links'] and request.POST['links'].strip()):
                recruiter.links = request.POST['links'].strip()
            request.user.save()
            recruiter.save()
        return redirect('home.index')
    else:
        template_data = {}
        template_data['degreeTypes'] = DegreeType.choices
        return render(request, 'accounts/onboard.html', {'template_data': template_data})


# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Accounts'
    return render(request, 'accounts/index.html', {'template_data': template_data})

# DELETE ME ON MERGE
def profiles(request):
    template_data = {}
    template_data['title'] = 'Accounts'
    return render(request, 'accounts/index.html', {'template_data': template_data})

