# Generated by Django 5.1.5 on 2025-01-17 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='can_preview',
            field=models.BooleanField(default=False, help_text='If a user does not have access to course, can they preview this lesson'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('publish', 'PUBLISH'), ('soon', 'Coming Soon'), ('draft', 'DRAFT')], default='publish', max_length=10),
        ),
    ]