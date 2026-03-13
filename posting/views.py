from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, IntegerField, Value
from applications.views import apply
from django.conf import settings

from skills.models import Skill
from accounts.models import Recruiter, JobSeeker
from .models import Post
from .tables import ApplicationsTable
from applications.models import Application
from home.notifications import update_post_notifications
from home.distance import longlatdistance
import csv
from django.http import HttpResponse



def index(request):
    postings = Post.objects.all()

    search = request.GET.get('search', '').strip()
    location_search = request.GET.get('location', '').strip()
    distance_between = request.GET.get('distance_between')
    job_type = request.GET.get('job_type')
    location_type = request.GET.get('location_type')
    visa = request.GET.get('visa')
    use_salary = request.GET.get('use_salary')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    skill_ids = request.GET.getlist('skills')
    if skill_ids:
        postings = postings.filter(skills__id__in=skill_ids).distinct()

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

    if distance_between:
        posting_list = []
        for posting in postings:
            if not request.user.is_anonymous and posting.latitude and posting.longitude:
                if longlatdistance(request.user, posting) <= int(distance_between):
                    posting_list.append(posting.id) 
        postings = postings.filter(pk__in=posting_list)

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
        'distance_choices': [('10', '10 Miles'), ('30', '30 Miles'), ('50', '50 Miles'), ('100', '100 Miles'),],
        'filter_job_type': job_type,
        'filter_location_type': location_type,
        'filter_visa': visa,
        'filter_salary_min': salary_min,
        'filter_salary_max': salary_max,
        'filter_use_salary': use_salary,
        'is_recruiter': is_recruiter,
        'google_api_key': settings.GOOGLE_API_KEY,
        'skills': Skill.objects.all().order_by('name'),
        'filter_skills': skill_ids,
    }

    return render(request, 'posting/index.html', {'template_data': template_data})
    
def build_filter_queryset(request, post):
    queryset = Application.objects.filter(posting=post)
    search = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    skills_filter = request.GET.get('skills', '').strip()
    if search:
        queryset = queryset.filter(Q(applicant__first_name__icontains=search) | Q(applicant__last_name__icontains=search))
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if skills_filter:
        queryset = queryset.filter(applicant__jobseeker__skills__name=skills_filter)
    sort_param = request.GET.get('sort', 'applicant__first_name')
    SORT_MAP = {
        'applicant__first_name': ('applicant__first_name', 'applicant__last_name'),
        '-applicant__first_name': ('-applicant__first_name', '-applicant__last_name'),
        'status': ('status',),
        '-status': ('-status',),
        'message': ('message',),
        '-message': ('-message',),
    }
    order_by = SORT_MAP.get(sort_param, ('applicant__first_name', 'applicant__last_name'))
    queryset = queryset.order_by(*order_by)
    return queryset


def post(request, id):
    post = get_object_or_404(Post, id=id)

    is_seeker = False
    user_details_hidden = False

    user = None
    
    if request.user.is_authenticated: 
        if JobSeeker.objects.filter(user=request.user).exists():
            user = JobSeeker.objects.filter(user=request.user)[0]
            if (user.account_is_hidden or user.education_is_hidden or user.experience_is_hidden or user.links_is_hidden):
                user_details_hidden = True

    template_data = {
        'title': f"{post.company_name} - {post.job_title}",
        'post': post,
        'id': id,
        'is_seeker': is_seeker,
        'user': user,
        'user_details_hidden': user_details_hidden,
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

    print(request.POST)
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
        'google_api_key': settings.GOOGLE_API_KEY,
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
        'google_api_key': settings.GOOGLE_API_KEY,
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
    posting.latitude = request.POST.get('latitude')
    posting.longitude = request.POST.get('longitude')
    posting.latitude = float(posting.latitude) if posting.latitude else None
    posting.longitude = float(posting.longitude) if posting.longitude else None

    if not posting.country:
        posting.location = 'No location specified'
    elif not posting.state:
        posting.location = posting.country.title()
    elif posting.state and not posting.city:
        posting.location = f"{posting.state.title()}, {posting.country.title()}"
    elif posting.city:
        posting.location = f"{posting.city.title()}, {posting.state.title()}"

    posting.save()

    skill_ids = request.POST.getlist('skills')
    if skill_ids:
        posting.skills.set(skill_ids)
    update_post_notifications(posting)

def export_csv(request):
    data = [['ID', 'Recruiter Name', 'Company', 'Position Title', 'City', 'Region', 'Country', 'Postal Code', 'Location', 'Date Posted', 'Salary Range', 'Job Type', 'Location Type', 'Visa Sponsorship', 'Skills Added', 'Applications Made']]
    all_posts = Post.objects.all()
    for post in all_posts:
        row = []
        row.append(post.id)
        row.append(f"{post.recruiter.user.first_name} {post.recruiter.user.last_name}")
        row.append(post.company_name)
        row.append(post.job_title)
        if post.city:
            row.append(post.city)
        else:
            row.append("")
        if post.state:
            row.append(post.state)
        else:
            row.append("")
        if post.country:
            row.append(post.country)
        else:
            row.append("")
        if post.postal_code:
            row.append(post.postal_code)
        else:
            row.append("")
        if post.location:
            row.append(post.location)
        else:
            row.append("")
        row.append(post.date_posted)
        if post.salary_min:
            row.append(f"${post.salary_min}k - ${post.salary_max}k")
        else:
            row.append("")
        row.append(post.job_type)
        row.append(post.location_type)
        row.append(post.visa_sponsorship)
        row.append(bool(post.skills))
        row.append(len(Application.objects.filter(posting=post)))

        data.append(row)
        print(row)

    file_path = 'posting/JobPostingData.csv'
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f'CSV file "{file_path}" created')
    if request.user.is_superuser:
        response = HttpResponse(open(file_path, 'rb'), content_type='text/csv')
        response['content-Disposition'] = 'attachment; filename="jobpostingdata.csv"'
        return response
    return redirect('accounts.index')
