from django.shortcuts import render

# Create your views here.

def index(request):
    template_data = {}
    template_data['title'] = 'Chat'
    return render(request, 'chat/index.html', {'template_data': template_data})