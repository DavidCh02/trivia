# models.py
from django.db import models
import random


class Question(models.Model):
    text = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)  # Debe coincidir con una de las opciones


    def get_answers(self):
        answers = [self.correct_answer, self.option_1, self.option_2, self.option_3, self.option_4]
        random.shuffle(answers)
        return answers


class Player(models.Model):
    name = models.CharField(max_length=15)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

