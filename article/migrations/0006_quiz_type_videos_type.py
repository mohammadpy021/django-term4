# Generated by Django 4.2.2 on 2024-04-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_remove_question_title_quiz_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='type',
            field=models.CharField(default='quiz', max_length=10, verbose_name='نوع'),
        ),
        migrations.AddField(
            model_name='videos',
            name='type',
            field=models.CharField(default='video', max_length=10, verbose_name='نوع'),
        ),
    ]
