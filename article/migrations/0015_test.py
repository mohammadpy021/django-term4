# Generated by Django 4.2.2 on 2024-05-01 17:24

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_quizprofile_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='گزینه های انتخاب شده توسط کاربر')),
            ],
        ),
    ]
