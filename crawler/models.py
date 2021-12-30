from django.db import models

# Create your models here.


class ContestInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    title_slug = models.CharField(max_length=250)
    start_time = models.CharField(max_length=250)


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    title_slug = models.CharField(max_length=250)
    score = models.IntegerField()
    contest = models.ForeignKey(
        to=ContestInfo, related_name="questions", on_delete=models.CASCADE
    )


class Contestant(models.Model):
    handle = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    # solved_problems = models.ManyToManyField(
    #     to=Question, related_name="solved_by", blank=True
    # )

class Contestant_Question(models.Model):
    contestant = models.ForeignKey(to=Contestant, related_name="attemped", on_delete=models.CASCADE, blank=False)
    question = models.ForeignKey(to=Question, related_name='solved_by', on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=50)
    timestamp = models.FloatField()
