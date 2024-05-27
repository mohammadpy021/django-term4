# Generated by Django 4.2.2 on 2024-04-30 19:15

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_remove_quizprofile_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizprofile',
            name='choices',
            field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='گزینه های انتخاب شده توسط کاربر'),
        ),
    ]
