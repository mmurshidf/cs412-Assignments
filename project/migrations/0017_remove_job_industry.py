# Generated by Django 5.1.3 on 2024-12-09 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_job_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='industry',
        ),
    ]