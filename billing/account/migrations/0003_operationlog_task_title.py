# Generated by Django 5.0.3 on 2024-03-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_operationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationlog',
            name='task_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]