# File: apps.py
# Author: Mohammed Murshid (murshidm@bu.edu), 12/9/2024
# Description: App

from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
