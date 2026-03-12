from django.db import models
from skills.models import Skill
from accounts.models import Recruiter, Education
import os
from django.utils.text import slugify

def get_image_path(post, filename):
    filetype = filename.split('.')[-1]
    new_name = slugify(post.company_name) + '.' + filetype
    return os.path.join('post_images', new_name) 

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, editable=False)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=get_image_path, default='post_images/default_job_posting.jpg')
    skills = models.ManyToManyField(Skill, blank = True, related_name='posts')
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
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
    def save(self, *args, **kwargs):
        if self.recruiter:
            self.company_name = self.recruiter.company
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.id) + ' - ' + self.company_name + ' - ' + self.job_title

class Query(models.Model):
    id = models.AutoField(primary_key=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True)
    distance = models.IntegerField(blank=True)
    #def __str__(self):
    #    return f"{skill.name for skill in self.skills.all()} and {f"{str(distance)} miles away." if distance < 25000 else "worldwide"}."