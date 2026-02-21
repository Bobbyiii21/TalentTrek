from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from .models import TTUser, JobSeeker, Recruiter
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import JobSeeker, Recruiter, Education, Experience
from skills.models import Skill

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
            request.user.is_seeker = True 
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
            request.user.is_recruiter = True 
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
        return redirect('accounts.profiles', user_link=str(request.user))
    else:
        template_data = {}
        return render(request, 'accounts/onboard.html', {'template_data': template_data})

def profiles(request, user_link):
    id = TTUser.get_id_by_name(user_link)
    user = TTUser.objects.get(id=id) 
    template_data = {}
    template_data['title'] = 'Profiles'
    template_data['profile_user'] = user
    template_data['id'] = id
    template_data['is_seeker'] = user.is_seeker
    template_data['is_recruiter'] = user.is_recruiter
    if template_data['is_seeker']:
        seeker_user = JobSeeker.objects.get(user_id=id)
        template_data["seeker_user"] = seeker_user
        template_data['education'] = seeker_user.education.all()
        template_data['skills'] = seeker_user.skills.all()
        template_data['skills_options'] = Skill.objects.all().order_by('name')
        template_data['experience'] = seeker_user.experience.all()
        template_data['degree_choices'] = Education.DegreeType.choices
        template_data['links'] = seeker_user.links.split(",")
        template_data['links'].pop()
        for link in template_data['links']:
            link = link.strip()
        #find some way to put resume 
    elif template_data['is_recruiter']:
        recruiter_user = Recruiter.objects.get(user_id=id)
        template_data['recruiter_user'] = recruiter_user
        template_data['links'] = recruiter_user.links.split(",")
        template_data['links'].pop()
        for link in template_data['links']:
            link = link.strip()


    if request.method == 'POST':
        updated = request.POST['subfield']
        if updated == 'headline':
            user.headline = request.POST['headline']
            user.save()

        if updated == 'pfp':
            request.user.pfp = request.FILES['pfp_upload'][0]
            
        elif user.is_seeker:
            if updated == 'hidden':
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

            if request.POST['subfield'] == 'education_add':
                try:
                    grad_year = request.POST['grad_year']
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()
                new_education = Education()
                new_education.grad_year = grad_year
                new_education.degree = request.POST['degree']
                new_education.degree_name = request.POST['degree_name']
                new_education.school_name = request.POST['school_name']
                new_education.save()
                seeker_user.education.add(new_education)
                return redirect('accounts.profiles', user_link=str(request.user))

            if request.POST['subfield'] == 'education_edit':
                try:
                    grad_year = request.POST['grad_year']
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()
                try:
                    edit_education = get_object_or_404(Education, id=request.POST['id'])
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()
                edit_education.grad_year = grad_year
                edit_education.degree = request.POST['degree']
                edit_education.degree_name = request.POST['degree_name']
                edit_education.school_name = request.POST['school_name']
                edit_education.save()
                return redirect('accounts.profiles', user_link=str(request.user))


            if request.POST['subfield'] == 'education_remove':
                try:
                    deleted_education = get_object_or_404(Education, id=request.POST['education_id'])
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()
                deleted_education.delete()
                return redirect('accounts.profiles', user_link=str(request.user))
            
            elif request.POST['subfield'] == 'experience_add':
                new_experience = Experience()
                new_experience.company_name = request.POST['company_name']
                new_experience.position_title = request.POST['position_title']
                new_experience.job_description = request.POST['job_description']
                new_experience.current_employee = bool(request.POST['current_employee'])
                new_experience.start_date = request.POST['start_date']
                if not new_experience.current_employee:
                    new_experience.end_date = request.POST['end_date']
                new_experience.save()
                seeker_user.experience.add(new_experience)
                return redirect('accounts.profiles', user_link=str(request.user))
            
            elif request.POST['subfield'] == 'experience_edit':
                try:
                    edit_experience = get_object_or_404(Experience, id=request.POST['id'])
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()

                edit_experience.company_name = request.POST['company_name']
                edit_experience.position_title = request.POST['position_title']
                edit_experience.job_description = request.POST['job_description']
                edit_experience.current_employee = bool(request.POST['current_employee'])
                edit_experience.start_date = request.POST['start_date']
                if not edit_experience.current_employee:
                    edit_experience.end_date = request.POST['end_date']
                edit_experience.save()
                return redirect('accounts.profiles', user_link=str(request.user))


            if request.POST['subfield'] == 'experience_remove':
                try:
                    deleted_experience = get_object_or_404(Experience, id=request.POST['experience_id'])
                except:
                    return redirect('home.index') #MAKE THIS A JS alert()
                deleted_experience.delete()
                return redirect('accounts.profiles', user_link=str(request.user))

            if request.POST['subfield'] == 'link_add':
                seeker_user.links += f"{request.POST['link'].strip()},"
                seeker_user.save()
                template_data['links'].append(request.POST['link'].strip())

            if request.POST['subfield'] == 'link_delete':
                seeker_user.links = seeker_user.links.replace(f"{request.POST['link'].strip()},", '')
                seeker_user.save()
                template_data['links'].remove(request.POST['link'])

            if request.POST['subfield'] == 'skill_add':
                for skill in request.POST['skills']:
                    seeker_user.skills.add(skill)
                seeker_user.save()
                
            if request.POST['subfield'] == 'skill_delete':
                skill = Skill.objects.get(id=request.POST['id'])
                seeker_user.skills.remove(skill)
                seeker_user.save()

        elif user.is_recruiter:
            if request.POST['subfield'] == 'link_add':
                recruiter_user.links += f"{request.POST['link'].strip()},"
                recruiter_user.save()
                template_data['links'].append(request.POST['link'].strip())

            if request.POST['subfield'] == 'link_delete':
                recruiter_user.links = recruiter_user.links.replace(f"{request.POST['link'].strip()},", '')
                recruiter_user.save()
                template_data['links'].remove(request.POST['link'])


    return render(request, 'accounts/profiles.html', {'template_data': template_data})

def index(request):
    profiles = TTUser.objects.all().order_by('first_name')
    template_data = {'profiles': profiles}
    return render(request, 'accounts/index.html', {'template_data': template_data})