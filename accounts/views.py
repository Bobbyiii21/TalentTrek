from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from .models import TTUser, JobSeeker, Recruiter
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

def profiles(request, user_link):
    id = TTUser.get_id_by_name(user_link)
    user = TTUser.objects.get(id=id) 
    template_data = {}
    template_data['title'] = 'Profiles'
    template_data['profile_user'] = user
    template_data['id'] = id
    template_data['is_seeker'] = False
    template_data['is_recruiter'] = False
    try:
        seeker_user = JobSeeker.objects.get(user_id=id)
        template_data['is_seeker'] = True
        template_data["seeker_user"] = seeker_user
        template_data['education'] = seeker_user.education.all()
        template_data['skills'] = seeker_user.education.all()
        template_data['experience'] = seeker_user.experience.all()
        template_data['links'] = seeker_user.links.split(",")
        for link in template_data['links']:
            link = link.strip()
        return render(request, 'accounts/profiles.html', {'template_data': template_data})
        #find some way to put resume
        
    except Exception:
        try:
            recruiter_user = Recruiter.objects.get(user_id=id)
            template_data['is_recruiter'] = True
            template_data['recruiter_user'] = recruiter_user
            template_data['links'] = recruiter_user.links.split(",")
            for link in template_data['links']:
                link = link.strip()
            return render(request, 'accounts/profiles.html', {'template_data': template_data})
        
        except Exception:
            return render(request, 'accounts/profiles.html', {'template_data': template_data})

@login_required
def edit_profile(request, user_link):
    id = TTUser.get_id_by_name(user_link)
    profile_user = get_object_or_404(TTUser, id=id)
    if request.user.id != profile_user.id:
        return redirect('accounts.profiles')
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = "Edit Profile"
        template_data['profile_user'] = profile_user
        template_data['is_seeker'] = True
        try:
            seeker_user = JobSeeker.objects.get(user_id=id)
            template_data['seeker_user'] = seeker_user
            template_data['education'] = seeker_user.education.all()
        except Exception:
            template_data['recruiter_user'] = Recruiter.objects.get(user_id=id)
            template_data['is_seeker'] = False
        return render(request, 'accounts/edit_profile.html', {'template_data': template_data})
    elif request.method == 'POST':
        profile_user.first_name = request.POST['first_name']
        profile_user.last_name = request.POST['last_name']
        profile_user.headline = request.POST['headline']
        profile_user.save()
        try:
            seeker_user = JobSeeker.objects.get(user_id=id)
            #for edu in template_data['education']:
            #    edu.grad_year = request.POST['grad_year']
            #    edu.school_name = request.POST['school_name']
                #figure out degree
            seeker_user.links = request.POST['links']
            #resume
            hidden_links = request.POST.getlist('hidden')
            if 'profile' in hidden_links:
                seeker_user.account_is_hidden = True
            else:
                seeker_user.account_is_hidden = False
            if 'experience' in hidden_links:
                seeker_user.experience_is_hidden = True
            else:
                seeker_user.experience_is_hidden = False
            if 'education' in hidden_links:
                seeker_user.education_is_hidden = True
            else:
                seeker_user.education_is_hidden = False
            if 'links' in hidden_links:
                seeker_user.links_is_hidden = True
            else:
                seeker_user.links_is_hidden = False
            seeker_user.save()
        except:
            recruiter_user = Recruiter.objects.get(user_id=id)
            recruiter_user.links = request.POST['links']
            recruiter_user.save()
        return redirect('accounts.profiles', user_link=user_link)
    else:
        return redirect('accounts.profiles', user_link=user_link)
