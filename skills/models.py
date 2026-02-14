from django.db import models

from enums.skills import Skills
# Create your models here.

class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name
