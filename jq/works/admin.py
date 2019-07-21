from django.contrib import admin
from .models import Job, Quest, Vote
# Register your models here.

admin.site.register(Quest)
admin.site.register(Job)
admin.site.register(Vote)
