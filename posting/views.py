from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, IntegerField, Value
from applications.views import apply

from skills.models import Skill
from accounts.models import Recruiter
from .models import Post
from .tables import ApplicationsTable
from applications.models import Application



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
            Q(job_title__icontains=search) |
            Q(company_name__icontains=search)
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
        
    is_recruiter = False
    if request.user.is_authenticated:
        is_recruiter = Recruiter.objects.filter(user=request.user).exists()

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
        'is_recruiter': is_recruiter,
    }

    return render(request, 'posting/index.html', {'template_data': template_data})


def post(request, id):
    post = get_object_or_404(Post, id=id)

    template_data = {
        'title': f"{post.company_name} - {post.job_title}",
        'post': post,
        'id': id,
    }

    # --
    template_data['skills'] = Skill.objects.all()
    if (request.user.is_authenticated and (Recruiter.objects.filter(user=request.user, company=post.company_name).exists())) or request.user.is_superuser:
        template_data['table_access'] = True
        queryset = build_filter_queryset(request, post)

        template_data['applications'] = ApplicationsTable(queryset)
    else:
        template_data['applications'] = None
        template_data['table_access'] = False
    return render(request, 'posting/post.html', {'template_data': template_data})


@login_required
def create(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)

    if request.method == 'POST':
        if request.POST.get('job_title', '').strip():
            posting = Post()
            posting.recruiter = recruiter
            posting.company_name = recruiter.company
            save_post(posting, request)
            return redirect('posting.index')

        return redirect('posting.index')

    skills = Skill.objects.all().order_by('name')
    return render(request, 'posting/create.html', {
        'skills': skills,
        'job_type_choices': Post.JOB_TYPE_CHOICES,
        'location_type_choices': Post.LOCATION_TYPE_CHOICES,
    })


@login_required
def edit(request, id):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    posting = get_object_or_404(Post, id=id, recruiter=recruiter)

    if request.method == 'POST':
        save_post(posting, request)
        return redirect('posting.post', id=posting.id)


    skills = Skill.objects.all().order_by('name')
    return render(request, 'posting/create.html', {
        'post': posting,
        'skills': skills,
        'job_type_choices': Post.JOB_TYPE_CHOICES,
        'location_type_choices': Post.LOCATION_TYPE_CHOICES,
        'editing': True,
    })


@login_required
def delete(request, id):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    posting = get_object_or_404(Post, id=id, recruiter=recruiter)
    posting.delete()
    return redirect('posting.index')

def save_post(posting, request):
    posting.job_title = request.POST.get('job_title', '').strip()
    posting.job_type = request.POST.get('job_type')
    posting.location_type = request.POST.get('location_type')
    posting.visa_sponsorship = 'visa_sponsorship' in request.POST
    posting.salary_min = request.POST.get('salary_min') or None
    posting.salary_max = request.POST.get('salary_max') or None

    posting.description = request.POST.get('description', '').strip()
    posting.description = posting.description or 'No description has been given for this posting.'

    if 'image' in request.FILES:
        posting.image = request.FILES['image']
    elif not posting.pk:
        posting.image = 'post_images/default_job_posting.jpg'

    posting.street = request.POST.get('street', '').strip()
    posting.city = request.POST.get('city', '').strip().title()
    posting.state = request.POST.get('state', '').strip().upper()
    posting.postal_code = request.POST.get('postal_code', '').strip()
    posting.country = request.POST.get('country', '').strip().title()

    if not posting.country:
        posting.location = 'No location specified'
    elif posting.state and not posting.city:
        posting.location = f"{posting.state}, {posting.country}"
    elif posting.city:
        posting.location = f"{posting.city}, {posting.state}"

    posting.save()

    skill_ids = request.POST.getlist('skills')
    if skill_ids:
        posting.skills.set(skill_ids)