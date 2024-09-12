# views.py
from django.shortcuts import render, redirect
from .forms import QuestionForm, AnswerForm, PlayerForm
from .models import Question, Player
import time
import os
from django.http import JsonResponse

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'trivia_game/add_question.html', {'form': form})

def play_game(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            request.session['player_id'] = player.id
            request.session[f'asked_questions_{player.id}'] = []
            return redirect('play_question')
    else:
        form = PlayerForm()
    return render(request, 'trivia_game/play_game.html', {'player_form': form})


def play_question(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('play_game')

    player = Player.objects.get(id=player_id)
    asked_questions_key = f'asked_questions_{player_id}'
    asked_questions = request.session.get(asked_questions_key, [])

    question_id = request.session.get(f'current_question_{player_id}')
    if question_id:
        question = Question.objects.get(id=question_id)
    else:
        question = Question.objects.exclude(id__in=asked_questions).order_by('?').first()

    if not question:
        return render(request, 'trivia_game/end_game.html', {
            'player': player,
            'message': '¡No hay más preguntas disponibles!',
        })

    result_message = ''
    result_class = ''
    show_next_button = False
    time_expired = False
    time_limit = 20  # Tiempo límite en segundos
    correct_answer = question.correct_answer  # Guardamos la respuesta correcta

    start_time = request.session.get(f'question_start_time_{player_id}')
    if not start_time:
        start_time = time.time()
        request.session[f'question_start_time_{player_id}'] = start_time

    elapsed_time = int(time.time() - start_time)
    time_left = max(0, time_limit - elapsed_time)

    if request.method == 'POST':
        form = AnswerForm(request.POST, question=question)

        # Manejar tiempo agotado
        if request.POST.get('time_expired') == 'true' or time_left <= 0:
            player.score -= 1
            result_message = f'¡Se acabó el tiempo! Has perdido 1 punto. La respuesta correcta era: {correct_answer}'
            result_class = 'incorrect'
            time_expired = True
            show_next_button = True
        elif form.is_valid():
            selected_answer = form.cleaned_data['selected_answer']
            if selected_answer == question.correct_answer:
                player.score += 10
                result_message = f'¡Respuesta Correcta! Has ganado 10 puntos. La respuesta correcta es: {correct_answer}'
                result_class = 'correct'
            else:
                player.score -= 5
                result_message = f'Respuesta Incorrecta. Has perdido 5 puntos. La respuesta correcta era: {correct_answer}'
                result_class = 'incorrect'

            show_next_button = True

        asked_questions.append(question.id)
        request.session[asked_questions_key] = asked_questions
        player.save()

        # Detener el temporizador
        del request.session[f'question_start_time_{player_id}']
        del request.session[f'current_question_{player_id}']

        # Establecer time_left a 0 para detener el temporizador en el frontend
        time_left = 0

    else:
        request.session[f'current_question_{player_id}'] = question.id
        form = AnswerForm(question=question)

    return render(request, 'trivia_game/play_question.html', {
        'form': form,
        'question': question,
        'player': player,
        'result_message': result_message,
        'result_class': result_class,
        'show_next_button': show_next_button,
        'time_left': time_left,
        'time_expired': time_expired,
        'correct_answer': correct_answer  # Pasamos la respuesta correcta al template
    })
def leaderboard(request):
    players = Player.objects.order_by('-score')
    return render(request, 'trivia_game/leaderboard.html', {'players': players})

def home(request):
    return render(request, 'trivia_game/home.html')

from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.http import require_POST

@require_POST
def load_data_view(request):
    try:
        # Carga los datos usando el comando 'loaddata'
        call_command('loaddata', 'preguntas2')  # Sin la ruta completa
        return HttpResponse("Datos cargados exitosamente.")
    except Exception as e:
        return HttpResponse(f"Error al cargar datos: {e}")
