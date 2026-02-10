from django.shortcuts import render

# Create your views here.

postings = [
    {
        'id': 1, 'name': 'Inception', 'price': 12,
        'description': 'A mind-bending heist thriller.'
    },
    {
        'id': 2, 'name': 'Avatar', 'price': 13,
        'description': 'A journey to a distant world and the battle for resources.'
    },
    {
        'id': 3, 'name': 'The Dark Knight', 'price': 14,
        'description': 'Gothams vigilante faces the Joker.'
    },
    {
        'id': 4, 'name': 'Titanic', 'price': 11,
        'description': 'A love story set against the backdrop of the sinking Titanic.',
    },
]
def index(request):
    template_data = {}
    template_data['title'] = 'Postings'
    template_data['postings'] = postings
    return render(request, 'posting/index.html',
                  {'template_data': template_data})
    
def post(request, id):
    post = postings[id - 1]
    template_data = {}
    template_data['title'] = post['name']
    template_data['post'] = post
    return render(request, 'posting/post.html',
                  {'template_data': template_data})