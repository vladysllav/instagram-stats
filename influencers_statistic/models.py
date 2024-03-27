from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
from influencers.models import BaseProfile


class StatisticsQuerySet(models.QuerySet):
    def get_period_statistics(self, user, date_start, date_end):
        return (
            self.filter(profile__user=user, created_at__date__range=(date_start, date_end))
            .order_by("profile", "-created_at")
            .distinct("profile")
        )

    def get_days_statistics(self, user, day_value):
        current_date = datetime.now().date()
        date_start = current_date - timedelta(days=day_value)
        date_end = current_date

        return self.get_period_statistics(user, date_start, date_end)


class StatisticsManager(models.Manager):
    def get_queryset(self):
        return StatisticsQuerySet(self.model)

    def get_period_statistics(self, user, date_start, date_end):
        return self.get_queryset().get_period_statistics(user, date_start, date_end)

    def get_days_statistics(self, user, period):
        return self.get_queryset().get_days_statistics(user, period.value)


class Statistics(models.Model):
    profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE, related_name="statistics")
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pictures = models.ImageField(upload_to="influencers/profile_images", null=True, blank=True)
    profile_pictures_url = models.TextField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    stats_manager = StatisticsManager()

    def __str__(self):
        return f"Statistics for {self.name}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.profile.pk})
