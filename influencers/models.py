"""This module contains the models for the influencers app."""
from django.db import models
from django.db.models.signals import post_save

from django.urls import reverse
from .signals import create_dynamic_profile_data
from django.contrib.auth.models import User


class BaseProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_profile = models.URLField(max_length=200, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = [['user', 'url_profile']]

post_save.connect(create_dynamic_profile_data, sender=BaseProfile)
