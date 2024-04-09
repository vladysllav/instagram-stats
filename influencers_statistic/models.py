from datetime import timedelta

from common.models.mixins import TimeStampedModel
from django.db import models
from django.db.models import F, OuterRef, Subquery
from django.urls import reverse
from django.utils import timezone
from influencers.models import BaseProfile


class StatisticsQuerySet(models.QuerySet):

    def get_start_end_statistics(self, user, date_start, date_end):
        return self._get_queryset_with_profiles(user, date_start, date_end)

    def _get_queryset_with_profiles(self, user, date_start, date_end):
        """
        Отримує queryset з профілями для обчислення зміни кількості фоловерів та відсоткової зміни за період.
        """

        current_date = timezone.now().date()
        if date_end > current_date:
            return None
        else:
            end_followers_subquery = Statistics.objects.filter(
                profile__user=user,
                created_at__date=date_end,
                profile=OuterRef("profile"),  # фільтр по профілю
            ).values("followers")[
                :1
            ]  # вибір останнього значення

            queryset = Statistics.objects.filter(
                profile__user=user,
                created_at__date__gte=date_start,
                created_at__date__lte=date_end,
            ).annotate(
                end_followers_number=Subquery(end_followers_subquery),
                followers_change_number=F("end_followers_number") - F("followers"),
                followers_change_percent=(F("followers_change_number") * 100.0) / F("followers"),
            )

            return self._order_queryset_by_end_followers_count(queryset)

    @staticmethod
    def _order_queryset_by_end_followers_count(queryset):
        """Повертає відсортований queryset з унікальними значеннями за датою створення"""
        return queryset.order_by("created_at").distinct()

    def get_days_statistics(self, user, day_value):
        current_date = timezone.now().date()
        date_start = current_date - timedelta(days=day_value)
        date_end = current_date

        return self.get_start_end_statistics(user, date_start, date_end)


class StatisticsManager(models.Manager):
    def get_queryset(self):
        return StatisticsQuerySet(self.model)

    def get_start_end_statistics(self, user, date_start, date_end):
        return self.get_queryset().get_start_end_statistics(user, date_start, date_end)

    def get_days_statistics(self, user, period):
        return self.get_queryset().get_days_statistics(user, period.value)


class Statistics(TimeStampedModel):
    profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE, related_name="statistics")
    name = models.CharField(max_length=50, null=True, blank=True)
    profile_pictures = models.ImageField(upload_to="influencers/profile_images", null=True, blank=True)
    profile_pictures_url = models.TextField(null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)

    objects = models.Manager()
    stats_manager = StatisticsManager()

    def __str__(self):
        return f"Statistics for {self.name}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.profile.pk})
