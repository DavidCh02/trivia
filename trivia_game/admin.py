
from django.contrib import admin
from .models import Question, Player

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_answer', 'option_1', 'option_2', 'option_3', 'option_4')
    search_fields = ('text', 'correct_answer')

class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'score')
    search_fields = ('player_name',)
    ordering = ('-score',)


admin.site.register(Question)
admin.site.register(Player)