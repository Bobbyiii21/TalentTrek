from django.shortcuts import render, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from .notifications import update_seeker_notifications
import ast

def index(request):
    template_data = {}
    template_data['title'] = 'Talent Trek'
    if (request.user.is_authenticated):
        notifications = Notification.objects.filter(recipient=request.user, read=False).order_by('date')
        template_data['notifications'] = notifications
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    return render(request, 'home/about.html')

@login_required
def notifications(request):
    template_data = {}
    template_data['title'] = 'Notifications'
    template_data['unread_notifications'] = Notification.objects.filter(recipient=request.user, read=False)
    template_data['read_notifications'] = Notification.objects.filter(recipient=request.user, read=True)
    #For Testing - if request.method == "POST": update_seeker_notifications(request.user)
    return render(request, 'home/notifications.html', {'template_data':template_data})

def notification_click(request, id):
    try:
        notification = Notification.objects.get(id=id)
        if request.user != notification.recipient:
            return redirect('home.index')
        notification.read = True
        notification.save()
        return redirect(notification.viewslink)
    except:
        return redirect('home.index')


