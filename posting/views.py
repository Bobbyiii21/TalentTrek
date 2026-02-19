from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from skills.models import Skill
from django.db.models import Q, Case, When, IntegerField, Value
from accounts.models import Recruiter

# Create your views here.
from .models import Post

def index(request):
    postings = Post.objects.all()
    search = request.GET.get('search', '').strip()
    location_search = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type')
    location_type = request.GET.get('location_type')
    visa = request.GET.get('visa')
    use_salary = request.GET.get('use_salary')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    
    if search:
        postings = postings.annotate(
            relevance=Case(
                When(job_title__icontains=search, then=Value(2)),
                When(company_name__icontains=search, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).filter(
            Q(job_title__icontains=search) | Q(company_name__icontains=search)
        ).order_by('-relevance', 'company_name')  
    if location_search:
        postings = postings.filter(
            Q(city__icontains=location_search) | 
            Q(state__icontains=location_search) | 
            Q(country__icontains=location_search)
        )
    if job_type:
        postings = postings.filter(job_type=job_type)
    if location_type:
        postings = postings.filter(location_type=location_type)
    if visa == 'on':
        postings = postings.filter(visa_sponsorship=True)
    if use_salary == 'on':
        if salary_min:
            postings = postings.filter(salary_min__gte=int(salary_min))
        if salary_max:
            postings = postings.filter(salary_max__lte=int(salary_max))
            
    if request.user.is_authenticated:
        my_postings = postings.filter(recruiter__user=request.user)
        other_postings = postings.exclude(recruiter__user=request.user)
    else:
        my_postings = Post.objects.none()
        other_postings = postings

    template_data = {
        'title': 'Postings',
        'postings': postings,
        'my_postings': my_postings,
        'other_postings': other_postings,
        'job_type_choices': Post.JOB_TYPE_CHOICES,
        'location_type_choices': Post.LOCATION_TYPE_CHOICES,
        'filter_job_type': job_type,
        'filter_location_type': location_type,
        'filter_visa': visa,
        'filter_salary_min': salary_min,
        'filter_salary_max': salary_max,
        'filter_use_salary': use_salary,
    }

    return render(request, 'posting/index.html', {'template_data': template_data})
    
def post(request, id):
    post = Post.objects.get(id=id)
    template_data = {}
    template_data['title'] = post.company_name + ' - ' + post.job_title
    template_data['post'] = post
    return render(request, 'posting/post.html',
                  {'template_data': template_data})

@login_required
def create(request):
    recruiter = Recruiter.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('job_title', '').strip() != '':
            posting = Post()
            posting.recruiter = recruiter
            posting.company_name = recruiter.company
            posting.job_title = request.POST.get('job_title', '').strip()
            posting.job_type = request.POST.get('job_type')
            posting.location_type = request.POST.get('location_type')
            posting.visa_sponsorship = 'visa_sponsorship' in request.POST
            posting.salary_min = request.POST.get('salary_min') or None
            posting.salary_max = request.POST.get('salary_max') or None
            if request.POST['description'] != '':
                posting.description = request.POST['description'].strip()
            posting.description = posting.description or 'No description has been given for this posting.'
            if 'image' in request.FILES:
                posting.image = request.FILES['image']
            else:
                posting.image = 'post_images/default_job_posting.jpg'
            
            posting.street = request.POST.get('street', '').strip()
            posting.city = request.POST.get('city', '').strip().title()
            posting.state = request.POST.get('state', '').strip().upper()
            posting.postal_code = request.POST.get('postal_code', '').strip()
            posting.country = request.POST.get('country', '').strip().title()
            if posting.country == '':
                posting.location = 'No location specified'
            elif posting.state != '' and posting.city == '':
                posting.location = f"{posting.state}, {posting.country}"
            elif posting.city != '':
                posting.location = f"{posting.city}, {posting.state}"
            
            posting.save()
            
            skill_ids = request.POST.getlist('skills')
            if skill_ids:
                posting.skills.set(skill_ids)
            return redirect('posting.index')
        else:
            return redirect('posting.index')
    else:
        skills = Skill.objects.all().order_by('name')
        return render(request, 'posting/create.html', {
            'skills': skills,
            'job_type_choices': Post.JOB_TYPE_CHOICES,
            'location_type_choices': Post.LOCATION_TYPE_CHOICES
        })