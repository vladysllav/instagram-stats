from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .signals import create_dynamic_profile_data

from utils import get_profile_photo, get_profile_followers
#


class BaseProfile(models.Model):
    url_profile = models.URLField(max_length=200, unique=True, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})


post_save.connect(create_dynamic_profile_data, sender=BaseProfile)

#
# class DynamicProfileData(models.Model):
#     base_profile = models.OneToOneField(BaseProfile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     profile_pictures = models.ImageField(upload_to="influencers/profile_images", null=True, blank=True)
#     followers = models.IntegerField(null=True, blank=True)
#
#     def get_absolute_url(self):
#         return reverse('profile_detail', kwargs={'pk': self.base_profile.pk})
#
#
