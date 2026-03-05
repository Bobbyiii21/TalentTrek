from .models import Notification

def base_data(request):
    base_data = {}
    if request.user.is_authenticated:
        base_data['base_data_notifications'] = Notification.objects.filter(recipient=request.user, read=False)
    return base_data
