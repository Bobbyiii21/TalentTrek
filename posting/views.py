from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from applications.views import apply
from django.db.models import Q

# Create your views here.
from .models import Post
from accounts.models import Recruiter
from .tables import ApplicationsTable
from applications.models import Application
from skills.models import Skill



def index(request):
    search_term = request.GET.get('search')
    if search_term:
        postings = Post.objects.filter(company_name__icontains=search_term)
    else:
        postings = Post.objects.all()
    template_data = {}
    template_data['title'] = 'Postings'
    template_data['postings'] = postings
    return render(request, 'posting/index.html',
                  {'template_data': template_data})
    
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
    post = Post.objects.get(id=id)
    template_data = {}
    template_data['title'] = post.company_name + ' - ' + post.job_title
    template_data['post'] = post
    template_data['id'] = id
    # --
    template_data['skills'] = Skill.objects.all()
    if (request.user.is_authenticated and (Recruiter.objects.filter(user=request.user, company=post.company_name).exists())) or request.user.is_superuser:
        template_data['table_access'] = True
        queryset = build_filter_queryset(request, post)

        template_data['applications'] = ApplicationsTable(queryset)
    else:
        template_data['applications'] = None
        template_data['table_access'] = False
    return render(request, 'posting/post.html',
                  {'template_data': template_data})

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['job_title'] != '' and request.POST['company_name'] != '':
            posting = Post()
            posting.company_name = request.POST['company_name']
            posting.job_title = request.POST['job_title']

            if request.POST['description'] != '':
                posting.description = request.POST['description']
            else:
                posting.description = 'No description has been given for this posting.'

            posting.image = request.FILES['image']
            posting.save()
            return redirect('posting.index')
        else:
            return redirect('posting.index')
    else:
        return render(request, 'posting/create.html')