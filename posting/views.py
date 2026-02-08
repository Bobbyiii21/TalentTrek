from django.shortcuts import render
def index(request):
    template_data = {}
    template_data['title'] = 'Job Postings'
    return render(request, 'home/posting.html', {'template_data': template_data})
# Create your views here.

# Create your views here.
