from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from influencers.models import BaseProfile
from influencers_statistic.models import Statistics
from utils import get_profile_followers, get_profile_photo, get_save_profile_pictures


class BaseStatistic(ListView):
    model = Statistics
    context_object_name = 'statistics'
    template_name = 'influencers_statistic/statistics.html'
    extra_context = {'title': 'STATISTICS'}

    def get_queryset(self):
        username = self.kwargs.get('name')
        if username:
            return Statistics.objects.filter(username=username).order_by('name', '-created_at').distinct('name')
        return Statistics.objects.all().order_by('name', '-created_at').distinct('name')


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


