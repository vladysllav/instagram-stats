from datetime import datetime, timedelta

from default_auth.views import OwnProfileMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView
from influencers.models import BaseProfile
from influencers_statistic.enums import StatisticsDaysEnum
from influencers_statistic.models import Statistics
from utils import client


class BaseStatistic(LoginRequiredMixin, OwnProfileMixin, ListView):
    model = Statistics
    context_object_name = "statistics"
    template_name = "influencers_statistic/statistics.html"
    extra_context = {"title": "STATISTICS"}

    def get_queryset(self):
        current_user = self.request.user
        sort_by = self.request.GET.get("sort_by")
        order = self.request.GET.get("order", "desc")
        queryset = Statistics.objects.filter(profile__user=current_user)

        # Сортировка queryset в соответствии с параметрами сортировки
        if sort_by == "followers":
            queryset = queryset.order_by("-followers" if order == "desc" else "followers")
        elif sort_by == "created_at":
            queryset = queryset.order_by("-created_at" if order == "desc" else "created_at")
        else:
            queryset = queryset.order_by("name", "-created_at").distinct("name")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by")
        context["order"] = self.request.GET.get("order", "desc")
        return context


class PeriodStatistic(LoginRequiredMixin, OwnProfileMixin, ListView):
    model = Statistics
    context_object_name = "statistics_period"
    template_name = "influencers_statistic/period_statistics.html"
    extra_context = {"title": "Filter by period statistics"}

    def get_queryset(self):
        current_user = self.request.user
        period = self.request.GET.get("period")

        statistics_manager = Statistics.stats_manager

        if period == "last_7_days":
            stats = statistics_manager.get_days_statistics(current_user, StatisticsDaysEnum.seven_days)
        elif period == "last_90_days":
            stats = statistics_manager.get_days_statistics(current_user, StatisticsDaysEnum.ninety_days)
        else:
            date_start = self.request.GET.get("date_start")
            date_end = self.request.GET.get("date_end")

            if date_start and date_end:
                date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
                date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
                if date_start > date_end:
                    return Statistics.objects.none()
            else:
                current_date = datetime.now().date()
                date_start = current_date - timedelta(days=30)
                date_end = current_date

            stats = statistics_manager.get_period_statistics(current_user, date_start, date_end)

        start_followers = {stat.profile_id: stat.followers for stat in stats}
        statistics_period = []
        for stat in stats:
            profile_id = stat.profile_id
            profile_photo = (
                Statistics.objects.filter(profile=profile_id).order_by("-created_at").first().profile_pictures
            )
            name = stat.name
            followers_start = start_followers.get(profile_id, 0)
            followers_end = stat.followers
            followers_change = followers_end - followers_start
            followers_change_percent = ((followers_change / followers_start) * 100) if followers_start else 0

            statistics_period.append(
                {
                    "profile_pictures": profile_photo,
                    "profile_id": profile_id,
                    "name": name,
                    "followers_start": followers_start,
                    "followers_end": followers_end,
                    "followers_change": followers_change,
                    "followers_change_percent": followers_change_percent,
                }
            )

        # Сортировка результатов
        statistics_period.sort(key=lambda x: x["followers_end"], reverse=True)
        return statistics_period

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_start"] = self.request.GET.get("date_start")
        context["date_end"] = self.request.GET.get("date_end")
        context["period"] = self.request.GET.get("period")
        return context


class ProfileStatsUpdater:
    def __init__(self, profile_id):
        self.profile_id = profile_id
        self.profile = BaseProfile.objects.get(pk=self.profile_id)
        self.profile_data = self.profile.statistics.first()

    def add_statistics(self):
        followers = client.get_profile_followers(self.profile_data.name)

        if self.profile_data.profile_pictures_url != client.get_profile_photo(self.profile_data.name):
            profile_pictures = client.get_save_profile_pictures(self.profile_data.name)
            profile_pictures_url = client.get_profile_photo(self.profile_data.name)
        else:
            profile_pictures = self.profile_data.profile_pictures
            profile_pictures_url = self.profile_data.profile_pictures_url

        Statistics.objects.update_or_create(
            profile=self.profile,
            defaults={
                "name": self.profile_data.name,
                "profile_pictures": profile_pictures,
                "profile_pictures_url": profile_pictures_url,
                "followers": followers,
            },
        )


def update_statistic_view(request):
    profiles = BaseProfile.objects.all()
    for profile in profiles:
        updater = ProfileStatsUpdater(profile.pk)
        updater.add_statistics()
    print("fireeeee")
    return HttpResponse("fireeeee")
