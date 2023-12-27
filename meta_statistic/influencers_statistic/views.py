from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from influencers.models import BaseProfile
from influencers_statistic.models import Statistics
from utils import get_profile_followers, get_profile_photo, get_save_profile_pictures
from django.db.models import Min, Max, OuterRef, Subquery
from collections import defaultdict
from django.db.models import F


class BaseStatistic(ListView):
    model = Statistics
    context_object_name = 'statistics'
    template_name = 'influencers_statistic/statistics.html'
    extra_context = {'title': 'STATISTICS'}


    def get_queryset(self):
        username = self.kwargs.get('name')
        if username:
            return Statistics.objects.filter(username=username)
        return Statistics.objects.all()


class ProfileStatsUpdater:
    def __init__(self, profile_id):
        self.profile_id = profile_id
        self.profile = BaseProfile.objects.get(pk=self.profile_id)
        self.profile_data = self.profile.statistics.first()

    def add_statistics(self):
        followers = get_profile_followers(self.profile_data.name)

        if self.profile_data.profile_pictures_url != get_profile_photo(self.profile_data.name):
            profile_pictures = get_save_profile_pictures(self.profile_data.name)
            profile_pictures_url = get_profile_photo(self.profile_data.name)
        else:
            profile_pictures = self.profile_data.profile_pictures
            profile_pictures_url = self.profile_data.profile_pictures_url

        new_statistics_entry = Statistics(
            profile=self.profile,
            name=self.profile_data.name,
            profile_pictures=profile_pictures,
            profile_pictures_url=profile_pictures_url,
            followers=followers,
        )

        new_statistics_entry.save()


def update_statistic(request):
    profiles = BaseProfile.objects.all()
    for profile in profiles:
        updater = ProfileStatsUpdater(profile.pk)
        updater.add_statistics()
    print("fireeeee")
    return HttpResponse("fireeeee")


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        # Получаем список уникальных пользователей
        profiles = BaseProfile.objects.all()

        # Получаем статистику по фоловерам для каждого пользователя за обе даты
        followers_stats_25 = Statistics.objects.filter(profile__in=profiles, created_at__date='2023-12-25')
        followers_stats_27 = Statistics.objects.filter(profile__in=profiles, created_at__date='2023-12-27')

        # Объединяем данные статистики
        followers_stats = followers_stats_25 | followers_stats_27

        # Создаем контекст данных для передачи в шаблон
        context = {
            'profiles': profiles,
            'followers_stats': followers_stats,
        }
        return render(request, 'influencers_statistic/statistics_table.html', context)