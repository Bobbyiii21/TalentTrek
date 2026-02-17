from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    template_data = {}
    template_data['title'] = 'Job Postings'
    return render(request, 'posting/index.html', {'template_data': template_data})

@login_required
def create(request):
    template_data = {}
    template_data['title'] = 'Create a Job Posting'
    return render(request, 'posting/create.html', {'template_data': template_data})

@login_required
def explore(request):
    template_data = {}
    template_data['title'] = 'Explore Job Postings'
    return render(request, 'posting/explore.html', {'template_data': template_data})