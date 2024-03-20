from django.db import models
from django.urls import reverse
from influencers.models import BaseProfile


class Statistics(models.Model):
    profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE, related_name="statistics")
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pictures = models.ImageField(upload_to="influencers/profile_images", null=True, blank=True)
    profile_pictures_url = models.TextField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Statistics for {self.name}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.profile.pk})
