# Generated by Django 4.2.2 on 2024-05-01 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_test'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test',
            new_name='MyTestClass',
        ),
    ]