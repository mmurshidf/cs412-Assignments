# Generated by Django 5.1.3 on 2024-11-22 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('profile', models.TextField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.account'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
