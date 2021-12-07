from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import requests
from django.http import HttpResponse

from crawler.models import Contestant, Question, ContestInfo
import json
import time

# Create your views here.


def home(request):
    currentTime = time.time()
    if request.method == "GET":
        contests = ContestInfo.objects.order_by("start_time").all().reverse()
        contestants = Contestant.objects.all()
        context = {
            "users" : [],
            "contests" : [],
        }
        for contestant in contestants:
            contestant_solved_problems = Question.objects.filter(solved_by=contestant)
            
            myContests = []
            for contest in contests:
                solved_problems = contestant_solved_problems.filter(
                    contest__id=contest.id
                )
                
                hasSolved = ["no", "no", "no", "no"]
                for problem in solved_problems:
                    hasSolved[problem.score-3] = "yes"

                myContests.append({
                    "contestName" : contest.title,
                    "hasSolved" : hasSolved
                })

            context["users"].append({
                "name" : contestant.name,
                "contests" : myContests
            })
        
        for contest in contests:
            context["contests"].append({
                "title" : contest.title,
                "titleSlug": contest.title_slug,
                "startTime" : contest.start_time,
                "endTime" : time.asctime(time.localtime(float(contest.start_time) + 5400)),
                "virtualEndTime" : float(contest.start_time) + 604800,
                "remainingTime" : float(contest.start_time) + 604800 - currentTime,
                "hasEnded" : True if currentTime - float(contest.start_time) >=5400 else False,
                "hasVirtualEnded" : True if currentTime - float(contest.start_time) >=604800 else False
            })
        return render(request, "crawler/home.html",{"context" : context})
    else:
        if request.POST.get("contest-id"):
            response = requests.get(
                "https://leetcode.com/contest/api/info/weekly-contest-"
                + request.POST.get("contest-id")
                + "/"
            ).json()
            print(
                time.asctime(time.localtime(response["contest"]["start_time"])),
                "contest time",
            )
            print(time.asctime(time.localtime(time.time())), "local time")
            if response["contest"]["start_time"] < time.time():
                contest_id = response["contest"]["id"]
                contest_title = response["contest"]["title"]
                contest_title_slug = response["contest"]["title_slug"]
                contest_start_time = response["contest"]["start_time"]
                # print("time ", response["contest"]["start_time"], contest_start_time)
                newContest = ContestInfo(
                    id=contest_id,
                    title=contest_title,
                    title_slug=contest_title_slug,
                    start_time=contest_start_time,
                )
                newContest.save()

                for i in range(len(response["questions"])):
                    question_id = response["questions"][i]["question_id"]
                    question_title = response["questions"][i]["title"]
                    question_title_slug = response["questions"][i]["title_slug"]
                    question_score = response["questions"][i]["credit"]

                    newQuestion = Question(
                        id=question_id,
                        title=question_title,
                        title_slug=question_title_slug,
                        score=question_score,
                        contest=newContest,
                    )
                    newQuestion.save()
        # payload = {"query": "{allContests{\n    title\n    titleSlug\n    startTime}}"}
        # response = requests.post(
        #     url="https://leetcode.com/graphql",
        #     json=payload,
        # )
        # response = response.json()

        contests = ContestInfo.objects.all()
        context = {"contests": contests}
        return render(request, "crawler/home.html", context)


def ranklist(request, id):
    if request.method == "GET":
        questions = ContestInfo.objects.get(id=id).questions.all()

        users = Contestant.objects.all()
        for user in users:
            user_handle = user.handle
            payload = {
                "operationName": "getRecentSubmissionList",
                "variables": {"username": "Shahidul1004"},
                "query": "query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n",
            }
            # payload = {"query": "{allContests{\n    title\n    titleSlug\n    startTime}}"}
            response = requests.post(
                url="https://leetcode.com/graphql",
                json=payload,
            )
            response = response.json()
            for submission in response["data"]["recentSubmissionList"]:
                if submission["statusDisplay"] != "Accepted":
                    continue
                submitted_problem = Question.objects.filter(title=submission["title"])
                # print(submitted_problem)
                # title = solution["title"]

                for question in questions:
                    if question.title == submission["title"]:
                        user.solved_problems.set(submitted_problem)
                        print("found")

        # title = response["data"]["recentSubmissionList"][0][""]
        # print(response["data"]["recentSubmissionList"][0])

    return HttpResponse("<h1>jkdhfkdjfh</h1>")
