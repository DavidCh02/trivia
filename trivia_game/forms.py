from django import forms
from .models import Question, Player

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer', 'option_1', 'option_2', 'option_3', 'option_4']


from django.db import models
import random


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Player.objects.filter(name=name).exists():
            raise forms.ValidationError('El nombre del jugador ya está en uso. Por favor, elige otro nombre brother.')
        return name


class AnswerForm(forms.Form):
    selected_answer = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['selected_answer'].choices = [(answer, answer) for answer in question.get_answers()]
