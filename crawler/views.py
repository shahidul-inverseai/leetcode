from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import requests
from django.http import HttpResponse

from crawler.models import Contestant, Contestant_Question, Question, ContestInfo
import json
import time

def convert_time(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    # print("seconds value in hours:",hour)
    # print("seconds value in minutes:",min)
    return "%02d:%02d:%02d" % (hour, min, sec) 

def home(request):
    currentTime = time.time()
    context = {
        "contests": []
    }
    if request.method == "POST":
        response = requests.get(
                "https://leetcode.com/contest/api/info/weekly-contest-"
                + request.POST.get("contest-id")
                + "/"
            ).json()
        # print(response)
        if('error' in response.keys()):
            context['error'] = "Enter valid contest ID"
        elif response["contest"]["start_time"] < currentTime:
            contest_id = response["contest"]["id"]
            contest_title = response["contest"]["title"]
            contest_title_slug = response["contest"]["title_slug"]
            contest_start_time = response["contest"]["start_time"]
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

    contests = ContestInfo.objects.order_by("start_time").all().reverse()
    
    for contest in contests:
        # status = "Finished!"

        if currentTime - float(contest.start_time) < 604800:
            rem = convert_time(float(contest.start_time) + 604800 - currentTime)
            status = "Running\nremaining time " + rem
            # print(status)
        else:
            status = "Finished"# + time.asctime(time.localtime(float(contest.start_time) + 604800))
        context["contests"].append({
            "id": contest.id,
            "title": contest.title,
            # "start_time": contest.start_time,
            "status" : status
        })
    return render(request, "crawler/home.html", context = context)


def ranklist(request, id):
    context = {
        "id": id,
        "data": []
    }
    questions = ContestInfo.objects.get(id=id).questions.all()
    contestants = Contestant.objects.all()
    # print(request.method)
    if request.method == "POST":
        for contestant in contestants:
            payload = {
                "operationName": "getRecentSubmissionList",
                "variables": {"username": contestant.handle},
                "query": "query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n",
            }
            response = requests.post(
                url="https://leetcode.com/graphql",
                json=payload,
            )
            response = response.json()
            for submission in reversed(response["data"]["recentSubmissionList"]):
                # print("submission", submission)
                for ques in questions:
                    # print("    ques", ques)
                    if ques.title_slug == submission["titleSlug"]:
                        # print("found")
                        query = Contestant_Question.objects.filter(question=ques).filter(contestant = contestant)
                        # print("        query", query)
                        if submission['statusDisplay'] == "Accepted":
                            if query:
                                # print("acepted and query found")
                                query[0].status = "Accepted"
                                query[0].timestamp = submission["timestamp"]
                                query[0].save()
                            else:
                                # print("accepted but query not found")
                                new = Contestant_Question(contestant = contestant, question = ques, status = "Accepted", timestamp = submission["timestamp"])
                                new.save()
                        elif query:
                            if query[0].status == "Accepted":
                                continue
                            # print("not accepted and query found")
                            query[0].status = submission["statusDisplay"]
                            query[0].timestamp = submission["timestamp"]
                            # query.set(status = submission["statusDisplay"], timestamp = submission["timestamp"])
                            query[0].save()
                        else:
                            # print("not accepted and query not found")
                            new = Contestant_Question(contestant = contestant, question = ques, status = submission["statusDisplay"], timestamp = submission['timestamp'])
                            new.save()
                        # break
                    else:
                        pass 
                        # print("not found")
                # if submission["statusDisplay"] == "Accepted":
                #     for ques in questions:
                #         if ques.title_slug == submission.titleSlug:
                #             new_solve = Contestant_Question(
                #                 contestant, 
                #                 ques, 
                #                 submission['statusDisplay'], 
                #                 submission['timestamp']
                #             )
                #             new_solve.save()
                #             break

    
    for contestant in contestants:
        solved_list = contestant.attempted.all()
        timestamp = []
        status = []
        scores = 0
        for ques in questions:
            found = solved_list.filter(question=ques)
            if found:
                timestamp.append(found[0].timestamp)
                status.append(found[0].status)
                if(found[0].status=="Accepted"):
                    scores += ques.score
            else:
                timestamp.append(-1)
                status.append(-1)
        context['data'].append({
            "name": contestant.name,
            "handle": contestant.handle,
            "scores": scores,
            "timestamp": timestamp,
            "status": status
        })
    # print(context)
    return render(request, "crawler/ranklist.html", context)


     

# def home(request):
#     currentTime = time.time()
#     if request.method == "GET":
#         contests = ContestInfo.objects.order_by("start_time").all().reverse()
#         contestants = Contestant.objects.all()
#         context = {
#             "users" : [],
#             "contests" : [],
#         }
#         for contestant in contestants:
#             contestant_solved_problems = Question.objects.filter(solved_by=contestant)
            
#             myContests = []
#             for contest in contests:
#                 solved_problems = contestant_solved_problems.filter(
#                     contest__id=contest.id
#                 )
                
#                 hasSolved = ["no", "no", "no", "no"]
#                 for problem in solved_problems:
#                     hasSolved[problem.score-3] = "yes"

#                 myContests.append({
#                     "contestName" : contest.title,
#                     "hasSolved" : hasSolved
#                 })

#             context["users"].append({
#                 "name" : contestant.name,
#                 "contests" : myContests
#             })
        
#         for contest in contests:
#             context["contests"].append({
#                 "title" : contest.title,
#                 "titleSlug": contest.title_slug,
#                 "startTime" : contest.start_time,
#                 "endTime" : time.asctime(time.localtime(float(contest.start_time) + 5400)),
#                 "virtualEndTime" : float(contest.start_time) + 604800,
#                 "remainingTime" : float(contest.start_time) + 604800 - currentTime,
#                 "hasEnded" : True if currentTime - float(contest.start_time) >=5400 else False,
#                 "hasVirtualEnded" : True if currentTime - float(contest.start_time) >=604800 else False
#             })
#         return render(request, "crawler/home.html",{"context" : context})
#     else:
#         if request.POST.get("contest-id"):
#             response = requests.get(
#                 "https://leetcode.com/contest/api/info/weekly-contest-"
#                 + request.POST.get("contest-id")
#                 + "/"
#             ).json()
#             print(
#                 time.asctime(time.localtime(response["contest"]["start_time"])),
#                 "contest time",
#             )
#             print(time.asctime(time.localtime(time.time())), "local time")
#             if response["contest"]["start_time"] < time.time():
#                 contest_id = response["contest"]["id"]
#                 contest_title = response["contest"]["title"]
#                 contest_title_slug = response["contest"]["title_slug"]
#                 contest_start_time = response["contest"]["start_time"]
#                 # print("time ", response["contest"]["start_time"], contest_start_time)
#                 newContest = ContestInfo(
#                     id=contest_id,
#                     title=contest_title,
#                     title_slug=contest_title_slug,
#                     start_time=contest_start_time,
#                 )
#                 newContest.save()

#                 for i in range(len(response["questions"])):
#                     question_id = response["questions"][i]["question_id"]
#                     question_title = response["questions"][i]["title"]
#                     question_title_slug = response["questions"][i]["title_slug"]
#                     question_score = response["questions"][i]["credit"]

#                     newQuestion = Question(
#                         id=question_id,
#                         title=question_title,
#                         title_slug=question_title_slug,
#                         score=question_score,
#                         contest=newContest,
#                     )
#                     newQuestion.save()
#         # payload = {"query": "{allContests{\n    title\n    titleSlug\n    startTime}}"}
#         # response = requests.post(
#         #     url="https://leetcode.com/graphql",
#         #     json=payload,
#         # )
#         # response = response.json()

#         contests = ContestInfo.objects.all()
#         context = {"contests": contests}
#         return render(request, "crawler/home.html", context)


# def ranklist(request, id):
#     if request.method == "GET":
#         questions = ContestInfo.objects.get(id=id).questions.all()

#         users = Contestant.objects.all()
#         for user in users:
#             user_handle = user.handle
#             payload = {
#                 "operationName": "getRecentSubmissionList",
#                 "variables": {"username": "Shahidul1004"},
#                 "query": "query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n",
#             }
#             # payload = {"query": "{allContests{\n    title\n    titleSlug\n    startTime}}"}
#             response = requests.post(
#                 url="https://leetcode.com/graphql",
#                 json=payload,
#             )
#             response = response.json()
#             for submission in response["data"]["recentSubmissionList"]:
#                 if submission["statusDisplay"] != "Accepted":
#                     continue
#                 submitted_problem = Question.objects.filter(title=submission["title"])
#                 # print(submitted_problem)
#                 # title = solution["title"]

#                 for question in questions:
#                     if question.title == submission["title"]:
#                         user.solved_problems.set(submitted_problem)
#                         print("found")

#         # title = response["data"]["recentSubmissionList"][0][""]
#         # print(response["data"]["recentSubmissionList"][0])

#     return HttpResponse("<h1>jkdhfkdjfh</h1>")
