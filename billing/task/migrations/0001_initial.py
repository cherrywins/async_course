# Generated by Django 5.0.3 on 2024-03-16 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeadQueueTaskEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, null=True, unique=True)),
                ('name', models.CharField(editable=False, max_length=1024)),
                ('timestamp', models.DateTimeField()),
                ('task_id', models.UUIDField(editable=False, null=True, unique=True)),
                ('assignee_id', models.UUIDField(editable=False, null=True, unique=True)),
                ('data', models.JSONField()),
                ('sync_at', models.DateTimeField(default=None, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1024)),
                ('uuid', models.UUIDField(editable=False, null=True, unique=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.PositiveIntegerField(default=1, null=True)),
                ('reward', models.PositiveIntegerField(default=1, null=True)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee', to='account.account')),
            ],
        ),
    ]
