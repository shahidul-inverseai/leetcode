from django.contrib import admin

from crawler.models import ContestInfo, Contestant, Question

# Register your models here.

admin.site.register(ContestInfo)
admin.site.register(Question)
admin.site.register(Contestant)
