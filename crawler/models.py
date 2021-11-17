from django.db import models

# Create your models here.


class ContestInfo(models.Model):
    contest_id = models.IntegerField()
    title = models.CharField(max_length=250)
    title_slug = models.CharField(max_length=250)
    start_time = models.CharField(max_length=250)


class Question(models.Model):
    question_id = models.IntegerField()
    title = models.CharField(max_length=250)
    title_slug = models.CharField(max_length=250)
    score = models.IntegerField()
    contest = models.ForeignKey(
        to=ContestInfo, related_name='questions', on_delete=models.CASCADE)
