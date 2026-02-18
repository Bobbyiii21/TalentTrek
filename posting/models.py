from django.db import models
from skills.models import Skill

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', default='post_images/default_job_posting.jpg')
    skills = models.ManyToManyField(Skill, blank = True, related_name='posts')
    def __str__(self):
        return str(self.id) + ' - ' + self.company_name
