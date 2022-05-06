from django.contrib import admin
from .models import post
from .models import comment

# Register your models here.
admin.site.register(post)
admin.site.register(comment)