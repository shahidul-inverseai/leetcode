
from django.urls import path
from crawler.views import view
urlpatterns = [
    path('', view, name='view'),
]
