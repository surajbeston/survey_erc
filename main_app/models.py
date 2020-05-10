from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

class User(models.Model):
    email = models.EmailField(unique = True)
    full_name = models.CharField(max_length = 200)
    roll_number = models.CharField(max_length = 10, blank = True)
    image = models.CharField(max_length = 500)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question = models.CharField(max_length = 200)
    answer = models.CharField(max_length = 100)
    hover_duration = JSONField()
    time_duration = models.IntegerField()

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    in_question = models.IntegerField()
    last_questions = ArrayField(models.IntegerField(), blank = True)
    random_iter = models.IntegerField()
    track_time = models.DateTimeField(blank = True, null = True)


