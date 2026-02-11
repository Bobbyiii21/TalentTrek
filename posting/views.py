from django.shortcuts import render

# Create your views here.
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
    return render(request, 'posting/post.html',
                  {'template_data': template_data})