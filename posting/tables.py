import django_tables2 as tables
from django.utils.safestring import mark_safe

from applications.models import Application
from django.urls import reverse
from accounts.models import TTUser


class ApplicationsTable(tables.Table):
    applicant_name = tables.Column(accessor='applicant', verbose_name='Name',
        order_by=('applicant__first_name', 'applicant__last_name'))
    message = tables.Column(verbose_name='Message', accessor='message')
    skills = tables.Column(accessor='applicant', verbose_name='Skills', orderable=False)
    location = tables.Column(verbose_name='Location', accessor='applicant')
    resume = tables.Column(accessor='applicant', verbose_name='Resume', orderable=False)
    status = tables.TemplateColumn(
        verbose_name='Status',
        template_code='''
        <form method="post" action="{% url 'applications.update_status' application_id=record.id %}" class="d-inline">
          {% csrf_token %}
          <select name="status" class="form-select form-select-sm" onchange="this.form.submit()">
            <option value="Applied" {% if record.status == "Applied" %}selected{% endif %}>Applied</option>
            <option value="Reviewed" {% if record.status == "Reviewed" %}selected{% endif %}>Reviewed</option>
            <option value="Interview" {% if record.status == "Interview" %}selected{% endif %}>Interview</option>
            <option value="Offer" {% if record.status == "Offer" %}selected{% endif %}>Offer</option>
            <option value="Closed" {% if record.status == "Closed" %}selected{% endif %}>Closed</option>
          </select>
        </form>
        ''',
        order_by='status'
    )

    def render_location(self, value):
        try:
            if value.city and value.region and value.country:
                return value.city.name + ', ' + value.region.name + ', ' + value.country.name
            elif value.city and value.region:
                return value.city.name + ', ' + value.region.name
            elif value.city and value.country:
                return value.city.name + ', ' + value.country.name
            elif value.region and value.country:
                return value.region.name + ', ' + value.country.name
            else:
                return 'No location available'
        except Exception:
            return 'No location available'

    def render_applicant_name(self, value):
        try:
            url = reverse('accounts.profiles', kwargs={'user_link': value.slugify_name()})
            return mark_safe(f'<a href="{url}">{value.first_name} {value.last_name}</a>')
        except Exception:
            return value.first_name + ' ' + value.last_name + ' (unavailable)'

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
        model = Application
        fields = ('applicant_name', 'message', 'skills', 'location', 'resume', 'status')
        attrs = {'class': 'table table-striped table-bordered'}
        orderable = False