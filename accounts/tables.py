import django_tables2 as tables
from django.utils.safestring import mark_safe

from django.urls import reverse
from accounts.models import JobSeeker


class RecruiterViewTable(tables.Table):
    name = tables.Column(accessor='user', verbose_name='Name',
        order_by=('user__first_name', 'user__last_name'))
    skills = tables.Column(accessor='user', verbose_name='Skills')
    location = tables.Column(accessor='user', verbose_name='Location')
    resume = tables.Column(accessor='user', verbose_name='Resume')
    email = tables.TemplateColumn(
        verbose_name='Email',
        template_code='''
        <a class="primary-hover-btn" href="mailto:{{ record.user.email }}" style="margin-left: auto;"><i class="fas fa-envelope"></i></a>
        ''',
    )
    message = tables.TemplateColumn(
        verbose_name='Message',
        template_code='''
        <a class="primary-hover-btn" href="{% url 'chat.create_room' participant_id=record.user.id %}" style="margin-left: auto;"><i class="fas fa-message"></i></a>
        ''',
    )
    
    def render_name(self, value):
        try:
            url = reverse('accounts.profiles', kwargs={'user_link': value.slugify_name()})
            return mark_safe(f'<a href="{url}">{value.first_name} {value.last_name}</a>')
        except Exception:
            return value.first_name + ' ' + value.last_name + ' (unavailable)'

    def render_location(self, value):
        try:
            return value.location.replace('None', 'No location available')
        except Exception:
            return 'No location available'

    def render_skills(self, value):
        try:
            return ', '.join(s.name for s in value.jobseeker.skills.all())
        except Exception:
            return 'No skills available'
    
    def render_resume(self, value):
        try:
            resume = value.jobseeker.resume
            if resume:
                return mark_safe(f'<a href="{resume.url}" target="_blank" rel="noopener">View</a>')
        except Exception:
            pass
        return 'No resume available'

    class Meta:
        model = JobSeeker
        fields = ('name', 'skills', 'location', 'resume', 'email', 'message')
        attrs = {'class': 'table table-striped table-bordered'}
        orderable = False