# Generated by Django 5.1.3 on 2024-12-09 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_remove_account_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.TextField(blank=True, null=True),
        ),
    ]