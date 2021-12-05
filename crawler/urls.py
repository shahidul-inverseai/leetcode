from django.urls import path
from crawler.views import home, ranklist

urlpatterns = [
    path("contests/<int:id>", ranklist, name="ranklist"),
    path("", home, name="home"),
]
