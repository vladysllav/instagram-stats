from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from default_auth.views import OwnProfileMixin
from influencers.models import BaseProfile
from influencers_statistic.models import Statistics
from utils import client


class BaseStatistic(LoginRequiredMixin, OwnProfileMixin, ListView):
    model = Statistics
    context_object_name = 'statistics'
    template_name = 'influencers_statistic/statistics.html'
    extra_context = {'title': 'STATISTICS'}

    def get_queryset(self):
        current_user = self.request.user
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'desc')
        queryset = Statistics.objects.filter(profile__user=current_user)

        # Сортировка queryset в соответствии с параметрами сортировки
        if sort_by == 'followers':
            queryset = queryset.order_by('-followers' if order == 'desc' else 'followers')
        elif sort_by == 'created_at':
            queryset = queryset.order_by('-created_at' if order == 'desc' else 'created_at')
        else:
            queryset = queryset.order_by('name', '-created_at').distinct('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by')
        context['order'] = self.request.GET.get('order', 'desc')
        return context


class PeriodStatistic(LoginRequiredMixin, OwnProfileMixin, ListView):
    model = Statistics
    context_object_name = 'statistics_period'
    template_name = 'influencers_statistic/period_statistics.html'
    extra_context = {'title': 'Filter by period statistics'}

    def get_queryset(self):
        current_user = self.request.user
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        if date_start and date_end:
            date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
            date_end = datetime.strptime(date_end, '%Y-%m-%d').date()

            # Добавьте фильтрацию по текущему пользователю здесь
            start_stats = Statistics.objects.filter(
                profile__user=current_user,
                created_at__date__gte=date_start
            ).order_by('profile', 'created_at').distinct('profile').values('profile', 'followers', 'name', 'profile_pictures')

            end_stats = Statistics.objects.filter(
                profile__user=current_user,
                created_at__date__lte=date_end
            ).order_by('profile', '-created_at').distinct('profile').values('profile', 'followers', 'name', 'profile_pictures')

            start_followers = {stat['profile']: stat['followers'] for stat in start_stats}
            statistics_period = []
            for stat in end_stats:
                profile_id = stat['profile']
                profile_photo = Statistics.objects.filter(profile=profile_id).order_by('-created_at').first().profile_pictures
                name = stat['name']
                followers_start = start_followers.get(profile_id, 0)
                followers_end = stat['followers']
                followers_change = followers_end - followers_start
                followers_change_percent = ((followers_change / followers_start) * 100) if followers_start else 0

                statistics_period.append({
                    'profile_pictures': profile_photo,
                    'profile_id': profile_id,
                    'name': name,
                    'followers_start': followers_start,
                    'followers_end': followers_end,
                    'followers_change': followers_change,
                    'followers_change_percent': followers_change_percent,
                })

            # Сортировка результатов
            statistics_period.sort(key=lambda x: x['followers_end'], reverse=True)
            return statistics_period

        # Если даты не указаны, возвращаем пустой QuerySet
        return Statistics.objects.none()


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


