from django.db import models
from accounts.models import TTUser

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(TTUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=1023)
    #Image should just copy from source (existing posting or candidate)
    image = models.ImageField(height_field=None, width_field=None, blank=True)
    #Make sure the viewslink field is valid python code. Called as redirect(eval(viewslink)) later
    viewslink = models.CharField(max_length=31, blank=True)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
