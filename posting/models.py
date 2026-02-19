from django.db import models
from skills.models import Skill

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', default='post_images/default_job_posting.jpg')
    skills = models.ManyToManyField(Skill, blank = True, related_name='posts')
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    JOB_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
        ('TP', 'Temporary'),
        ('OT', 'Other'),
    ]
    LOCATION_TYPE_CHOICES = [
        ('ON', 'On-site'),
        ('HY', 'Hybrid'),
        ('RE', 'Remote'),
    ]
    job_type = models.CharField(
        max_length=2,
        choices=JOB_TYPE_CHOICES,
        default='FT'
    )
    location_type = models.CharField(
        max_length=2,
        choices=LOCATION_TYPE_CHOICES,
        default='ON'
    )
    visa_sponsorship = models.BooleanField(
        default=False
    )    
    def __str__(self):
        return str(self.id) + ' - ' + self.company_name
