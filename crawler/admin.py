from django.contrib import admin

from crawler.models import ContestInfo, Question

# Register your models here.

admin.site.register(ContestInfo)
admin.site.register(Question)
