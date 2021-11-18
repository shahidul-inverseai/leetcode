from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import requests
from django.http import HttpResponse

# Create your views here.


def crawlContest(request):
    response = requests.get("https://leetcode.com/contest/api/info/weekly-contest-267/")
    print(response.json())
    return render(request, "crawler/crawl_contest.html")
