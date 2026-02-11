from django.contrib import admin, messages
from .models import JobSeeker, Recruiter, Education, Experience
from django.utils.translation import ngettext
class JobSeekerAdmin(admin.ModelAdmin):
    ordering = ['email', 'first_name']
    search_fields = ['email', 'first_name']

class RecruiterAdmin(admin.ModelAdmin):
    actions = ["unreport"]
    
    @admin.action(description="Unhide selected reviews")
    def unreport(self, request, queryset):
        updated = queryset.update(is_reported=False)
        self.message_user(
            request,
            ngettext(
                "%d story was successfully marked as published.",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

# Register your models here.
admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Recruiter, RecruiterAdmin)
# Register your models here.
