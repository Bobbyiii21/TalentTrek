from django.db import models

# Create your models here.
from django.db import models
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.company_name