from django.contrib import admin

from crawler.models import ContestInfo, Contestant, Contestant_Question, Question

# Register your models here.

admin.site.register(ContestInfo)
admin.site.register(Question)
admin.site.register(Contestant)
admin.site.register(Contestant_Question)
