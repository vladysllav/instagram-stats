"""
Default auth app config
"""
from django.apps import AppConfig


class DefaultAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'default_auth'
