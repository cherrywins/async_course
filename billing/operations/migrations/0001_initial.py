# Generated by Django 5.0.3 on 2024-03-17 10:42

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_remove_payoutlog_account_delete_operationlog_and_more'),
        ('task', '0004_task_jira_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('is_processed', models.BooleanField(default=False, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker', to='account.account')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='task.task')),
            ],
        ),
        migrations.CreateModel(
            name='PayOutLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, null=True)),
                ('amount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='account.account')),
            ],
        ),
    ]
