from django.db import models
from accounts.models import TTUser
from posting.models import Post

MAX_LENGTH = 1000

class Application(models.Model):
    STATUS_CHOICES = {
        "Applied": "Applied",
        "Reviewed": "Reviewed",
        "Interview": "Interview",
        "Offer": "Offer",
        "Closed": "Closed"
    }

    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(TTUser, on_delete=models.CASCADE)
    posting = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField(max_length=MAX_LENGTH, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.applicant}: Application to {self.posting.job_title} at {self.posting.company_name}"