from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import TTUser
from posting.models import Post
from skills.models import Skill
from .models import Application
from accounts.models import Recruiter
from .tables import ApplicationsTable


@login_required
def index(request, view_mode=None):
    template_data = {}
    template_data['title'] = 'Applications'
    template_data['is_recruiter'] = TTUser.objects.get(id=request.user.id).is_recruiter

    if not template_data['is_recruiter']:
        template_data['applications'] = Application.objects.filter(applicant=request.user).order_by('-date')
    else:
        if (request.user.is_authenticated and (Recruiter.objects.filter(user=request.user).exists())) or request.user.is_superuser:
            template_data['table_access'] = True
            template_data['skills'] = Skill.objects.all()
            queryset = build_filter_queryset(request, request.user)
            template_data['applications'] = ApplicationsTable(queryset)
            template_data['applicants'] = queryset

        recruiter_applications = Application.objects.filter(posting__recruiter__user=request.user).order_by('-date')

        for choice in Application.STATUS_CHOICES:
            template_data[f"applications_{choice.lower()}"] = recruiter_applications.filter(status=choice)

        template_data['job_titles'] = []
        for application in recruiter_applications:
             if application.posting.job_title not in template_data['job_titles']:
                 template_data['job_titles'].append(application.posting.job_title)

        if view_mode is None or view_mode not in ('board', 'table', 'map'):
            template_data['view_mode'] = 'board'
        else:
            template_data['view_mode'] = view_mode
    return render(request, 'applications/index.html', {'template_data': template_data})

def build_filter_queryset(request, recruiter):
    queryset = Application.objects.filter(posting__recruiter__user=recruiter)
    search = request.GET.get('search', '').strip()
    job_title_filter = request.GET.get('job_title', '').strip()
    status_filter = request.GET.get('status', '').strip()
    skills_filter = request.GET.get('skills', '').strip()
    if search:
        queryset = queryset.filter(Q(applicant__first_name__icontains=search) | Q(applicant__last_name__icontains=search))
    if job_title_filter:
        queryset = queryset.filter(posting__job_title=job_title_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if skills_filter:
        queryset = queryset.filter(applicant__jobseeker__skills__name=skills_filter)
    sort_param = request.GET.get('sort', 'posting__job_title')
    SORT_MAP = {
        'posting__job_title': ('posting__job_title',),
        '-posting__job_title': ('-posting__job_title',),
        'applicant__first_name': ('applicant__first_name', 'applicant__last_name'),
        '-applicant__first_name': ('-applicant__first_name', '-applicant__last_name'),
        'status': ('status',),
        '-status': ('-status',),
        'message': ('message',),
        '-message': ('-message',),
    }
    order_by = SORT_MAP.get(sort_param, ('posting__job_title',))
    queryset = queryset.order_by(*order_by)
    return queryset

@login_required
def apply(request, posting_id):
    if request.method == 'POST':
        application = Application()
        application.applicant = TTUser.objects.get(id=request.user.id)
        application.posting = get_object_or_404(Post, id=posting_id)
        application.message = request.POST['message']
        application.save()
    return redirect('applications.index')

@login_required
def update_status(request, application_id, context):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        if (request.user.is_authenticated and (Recruiter.objects.filter(user=request.user, company=application.posting.company_name).exists())) or request.user.is_superuser:
            application.status = request.POST['status']
            application.save()
    if context == 'applications_page':
        return redirect('applications.index')
    if context == 'applications_page_table':
        return redirect('applications.index', view_mode='table')
    return redirect('posting.post', id=application.posting.id)
