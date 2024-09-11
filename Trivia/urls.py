from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trivia_game.urls')),  # Esto dirige la URL raíz a trivia_game.urls
]
