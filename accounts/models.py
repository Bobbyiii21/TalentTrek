from django.db import models
from cities_light.models import City, Country, Region #look up cities_light documentation if this isn't working, it hasn't been tested yet
from datetime import date
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.text import slugify
from skills.models import Skill
import os

#NOTE: some of these models may need to be moved into different apps in order to be integrated properly, dont forget import statments if necessary after moving
#NOTE: make sure to verify that we are using the same method of implementation for things such as locations, fix conflicts immediately

#File Upload naming schemes
def get_pfp_path(user, filename):
    filetype = filename.split('.')[-1]
    new_name = user.slugify_name() + '.' + filetype
    return os.path.join('pfps', new_name)

def get_resume_path(job_seeker, filename):
    filetype = filename.split('.')[-1]
    new_name = job_seeker.user.slugify_name() + '.' + filetype
    return os.path.join('resumes', new_name)



#might just create 2 separate user classes? depends on whether its easier to implement a parent class or have 2 independent user classes.
#parent class defines a User with an ID, username, email
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        user = self.model(email=email, first_name=first_name, last_name=last_name, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password):
        user = self.model(email=email, first_name=first_name, last_name=last_name, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)

class TTUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("first name", max_length=31)
    last_name = models.CharField("last_name", max_length=31)
    email = models.EmailField("email address", max_length=127, unique=True)
    link = models.SlugField(max_length=255, blank=True)
    pfp = models.ImageField(upload_to=get_pfp_path, height_field=None, width_field=None, blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True, null=True) #UNTESTED
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, blank=True, null=True) #UNTESTED
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=True, null=True) #UNTESTED 
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    headline = models.TextField(max_length=1023, blank=True)
    is_seeker = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    # Check that the above image loads and figure out where to store user-uploaded images
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
    )


    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomAccountManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = "Talent Trek User"
        verbose_name_plural = "Talent Trek Users"

    def slugify_name(self):
        return f"{slugify(self.first_name)}-{slugify(self.last_name)}-{str(self.id)}"

    def get_id_by_name(user_name):
        return int(user_name.split('-')[-1])

    def natural_key(self):
        return self.email


    def __str__(self):
        return self.slugify_name()


#NOTE: some of these models may need to be moved into different apps in order to be integrated properly, dont forget import statments if necessary after moving
#NOTE: make sure to verify that we are using the same method of implementation for things such as locations, fix conflicts immediately
#NOTE: hidden properties should be shown on the users own profile page with a flag showing they are hidden, and hide them from all other users.

#builds an education summary that will be displayed as one unified part of the profile
class DegreeType(models.TextChoices):
    HIGHSCHOOL = "HIGHSCHOOL", "High School"
    CERTIFICATE = "CERTIFICATE", "Certificate"
    ASSOCIATES = "ASSOCIATES", "Associate's"
    BACHELORS = "BACHELORS", "Bachelor's"
    MASTERS = "MASTERS", "Master's"
    DOCTORATE = "DOCTORATE", "Doctorate"

class Education(models.Model):
    grad_year = models.PositiveIntegerField() #if current student, they should put in projected grad date
    school_name = models.CharField(max_length=63)
    degree = models.CharField(choices=DegreeType.choices, max_length=15)

#builds a summary of a job experience
class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True) #use html/css to hide this if currently employed
    #Make sure to add a comment to user that date will not be displayed if they are currently employed.
    current_employee = models.BooleanField(default=False)
    company_name = models.CharField(max_length=63)
    position_title = models.CharField(max_length=63)
    job_description = models.TextField(max_length=511)


#children of User model for different account types below

#model for a job seeker
#TODO: add list of choices for skills somewhere (not in this app since they need to be used for search)
#TODO: verify if country and city works properly
#TODO: resume
class JobSeeker(models.Model):
    user = models.OneToOneField(TTUser, primary_key=True, on_delete=models.CASCADE)
    education = models.ManyToManyField(Education, blank=True) #list of education objects
    skills = models.ManyToManyField(Skill, blank=True)
    experience = models.ManyToManyField(Experience, blank=True) #job experience objects
    links = models.TextField(max_length=255, help_text="Please enter links as Comma Separated Values") #check if list implemented propery; implement as a list of links that the job seeker can input to relevant sites such as a personal site or linkedin, etc
    resume = models.FileField(upload_to=get_resume_path, blank=True)
    education_is_hidden = models.BooleanField(default=False)
    experience_is_hidden = models.BooleanField(default=False)
    links_is_hidden = models.BooleanField(default=False) #hides entire links field
    account_is_hidden = models.BooleanField(default=False) #hides everything except name and pfp with a message a la "this profile is hidden" if user profile is clicked on    

    def __str__(self):
        return str(self.user)
    
    REQUIRED_FIELDS = ['user']

    class Meta:
        verbose_name = "Job Seeker"

#model for a recruiter
class Recruiter(models.Model):
    user = models.OneToOneField(TTUser, primary_key=True, on_delete=models.CASCADE)
    company = models.TextField(max_length=63)
    links = models.TextField(max_length=255, help_text="Please enter links as Comma Separated Values", blank=True) #check if list implemented propery; implement as a list of links that the job seeker can input to relevant sites such as a personal site or linkedin, etc

    def __str__(self):
        return str(self.user)

    REQUIRED_FIELDS = ['user']

    class Meta:
        pass
