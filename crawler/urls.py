from django.urls import path
from crawler.views import ranklist, home

# urlpatterns = [
#     path("contests/<int:id>", ranklist, name="ranklist"),
#     path("", home, name="home"),
# ]

urlpatterns = [
    path("", home, name="home"),
    path("ranklist/<int:id>", ranklist, name='ranklist'),
]
