from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    User.objects.create_superuser('david', 'chingocriss703@gmail.com', '123456789')

class Migration(migrations.Migration):

    dependencies = [
        ('trivia_game', '0003_create_superuser'),  # Asegúrate de que esto apunte a tu última migración
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
