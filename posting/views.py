from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from applications.views import apply
from .models import Post

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
    
def post(request, id):
    post = Post.objects.get(id=id)
    template_data = {}
    template_data['title'] = post.company_name + ' - ' + post.job_title
    template_data['post'] = post
    template_data['id'] = id
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
