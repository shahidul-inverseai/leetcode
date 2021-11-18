from django.urls import path
from crawler.views import crawlContest

urlpatterns = [
    path("", crawlContest, name="crawl-contest"),
]
