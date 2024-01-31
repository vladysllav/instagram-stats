"""Influencers admin."""

from django.contrib import admin
from .models import BaseProfile


admin.site.register(BaseProfile)


