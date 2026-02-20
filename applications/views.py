from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import TTUser
from posting.models import Post
from .models import Application
from accounts.models import Recruiter

def index(request):
    template_data = {}
    template_data['title'] = 'Applications'
    template_data['is_recruiter'] = TTUser.objects.get(id=request.user.id).is_recruiter
    template_data['applications'] = Application.objects.filter(applicant=request.user).order_by('-date')
    return render(request, 'applications/index.html', {'template_data': template_data})

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
def update_status(request, application_id):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        if (request.user.is_authenticated and (Recruiter.objects.filter(user=request.user, company=application.posting.company_name).exists())) or request.user.is_superuser:
            application.status = request.POST['status']
            application.save()
    return redirect('posting.post', id=application.posting.id)
