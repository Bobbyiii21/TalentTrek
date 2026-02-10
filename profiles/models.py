from django.db import models
from cities_light.models import City, Region, Country #look up cities_light documentation if this isn't working, it hasn't been tested yet
from datetime import date
from django.contrib.auth.models import User

#NOTE: some of these models may need to be moved into different apps in order to be integrated properly, dont forget import statments if necessary after moving
#NOTE: make sure to verify that we are using the same method of implementation for things such as locations, fix conflicts immediately

#children of User model for different account types below


#model for a recruiter
#TODO: build the model? if it needs anything
class Recruiter(User):
    #tbh idk if this needs any unique variables, just unique permissions, so im not sure if i need to actually put anything here since its essential properties are in its parent
    pass


#model for a job seeker
#TODO: verify if lists of objects are implemented correctly and fix issues if not
#TODO: add list of choices for skills somewhere (not in this app since they need to be used for search)
#TODO: verify if country and city works properly
#TODO: use html/css to make "links" into hyperlinks
class JobSeeker(User):
    headline = models.TextField(max_length=1023)
    #skills = models.CharField(blank=True, choices=CHOICES, max_length=31) MAKE A LIST OF POSSIBLE SKILLS SOMEWHERE AND REPLACE "CHOICES" WITH APPROPRIATE VARIABLE
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True) #UNTESTED
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True) #UNTESTED
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True) #UNTESTED

class Education(models.Model):
    grad_year = models.PositiveIntegerField() #if current student, they should put in projected grad date
    school_name = models.CharField(max_length=63)
    degree_type = models.TextChoices("degree_type", "HIGHSCHOOL CERTIFICATE ASSOCIATES BACHELORS MASTERS DOCTORATE") #hopefully this is the way to implement a list of choices???
    degree = models.CharField(choices=degree_type, max_length=15)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

#builds a summary of a job experience
class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(default=date.today) #use html/css to hide this if currently employed
    #sets default to today if that is the case (this will force the user to put a date if they are not currently employed)
    #Make sure to add a comment to user that date will not be displayed if they are currently employed.
    current_employee = models.BooleanField(default=False)
    company_name = models.CharField(max_length=31)
    position_title = models.CharField(max_length=31)
    job_description = models.TextField(max_length=511)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

class Link(models.Model):
    url = models.URLField(max_length=127)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
