# Generated by Django 5.0.2 on 2024-03-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, default='assigned', max_length=255, null=True),
        ),
    ]
