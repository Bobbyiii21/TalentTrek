from django.shortcuts import render
<<<<<<< HEAD
# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Profiles'
    return render(request, 'profiles/index.html', {'template_data': template_data})
=======
>>>>>>> setup_wizard
# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Profiles'
    return render(request, 'profiles/index.html', {'template_data': template_data})
# Create your views here.

