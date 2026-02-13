from django.contrib import admin, messages
from .models import TTUser, JobSeeker, Recruiter, Education, Experience
from django.utils.translation import ngettext
class JobSeekerAdmin(admin.ModelAdmin):
    pass

class RecruiterAdmin(admin.ModelAdmin):
    pass

class TTUserAdmin(admin.ModelAdmin):
    ordering = ['id', 'email', 'first_name']
    search_fields = ['email', 'first_name']
    model = TTUser
    
# Register your models here.
admin.site.register(TTUser, TTUserAdmin)
admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Recruiter, RecruiterAdmin)
# Register your models here.
