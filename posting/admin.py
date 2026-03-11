from django.contrib import admin

# Register your models here.
from .models import Post, Query
admin.site.register(Post)
admin.site.register(Query)