from django.db import models

#NOTE: some of these models may need to be moved into different apps in order to be integrated properly, dont forget import statments if necessary after moving
#NOTE: make sure to verify that we are using the same method of implementation for things such as locations, fix conflicts immediately

#builds an education summary that will be displayed as one unified part of the profile
#TODO: test if degree type selection works properly when creating an education model
class Education(models.Model):
    grad_year = models.PositiveIntegerField(length=4) #if current student, they should put in projected grad date
    school_name = models.CharField(max_length=63)
    degree_type = models.TextChoices("degree_type", "HIGHSCHOOL CERTIFICATE ASSOCIATES BACHELORS MASTERS DOCTORATE") #hopefully this is the way to implement a list of choices???
    degree = models.CharField(choices=degree_type, max_length=15)

#builds a summary of a job experience
#TODO: hide end date if current employee
class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField() #find a way to hide this if currently employed
    current_employee = models.BooleanField(default=False)
    company_name = models.CharField(max_length=31)
    position_title = models.CharField(max_length=31)
    job_description = models.TextField(max_length=511)

#might just create 2 separate user classes? depends on whether its easier to implement a parent class or have 2 independent user classes.

#parent class defines a User with an ID, username, email
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=63)
    email = models.CharField(max_lenth=127)

#children of User model for different account types

#model for a job seeker
#TODO: verify if lists of objects are implemented correctly and fix issues if not
#TODO: add list of choices for skills somewhere (not in this app since they needs to be used for search)
#TODO: figure out how to add locations
#TODO: use html/css to make "links" into hyperlinks
class JobSeeker(User):
    headline = models.TextField(max_length=1023)
    education = models.ForeignKey([Education], on_delete=models.CASCADE) #list of education objects; this might need to be changed later, idrk how i should be implementing it as a list
    #skills = models.CharField(blank=True, choices=CHOICES, max_length=31) MAKE A LIST OF POSSIBLE SKILLS SOMEWHERE AND REPLACE "CHOICES" WITH APPROPRIATE VARIABLE
    experience = models.ForeignKey([Experience], on_delete=models.CASCADE) #list of job experience objects; might need to be changed with education
    links = [models.TextField(max_length=127)] #check if list implemented propery; implement as a list of links that the job seeker can input to relevant sites such as a personal site or linkedin, etc
    #location = idk how to add this

#model for a recruiter
#TODO: build model
class Recruiter(User):
    #tbh idk if this needs any unique variables, just unique permissions, so im not sure if i need to actually put anything here since its essential properties are in its parent
    pass


