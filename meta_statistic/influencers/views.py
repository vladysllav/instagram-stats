from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.urls import reverse_lazy, reverse
from django.views import View

from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import BaseUpdateView

from .models import BaseProfile
from .forms import ProfileForm
from utils import get_profile_photo, get_profile_followers


class BaseProfileCreateView(CreateView):
    form_class = ProfileForm
    template_name = 'influencers/profile_create.html'


# class BaseProfileDetailView(DetailView):
#     model = BaseProfile
#     template_name = 'influencers/profile_detail.html'
#     context_object_name = 'profile'

class BaseProfileDetailView(DetailView):
    model = BaseProfile
    template_name = 'influencers/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statistics'] = self.object.statistics.first()  # Fetch related Statistics object
        return context

def update_followers(profile_data_object, new_followers_count):
    """Обновляет поле followers в указанном объекте DynamicProfileData.

    Args:
        profile_data_object: Объект DynamicProfileData, для которого нужно обновить поле followers.
        new_followers_count: Новое значение количества подписчиков.
    """

    profile_data_object.followers = new_followers_count
    profile_data_object.save()

# def index(request):
#     profile_data = DynamicProfileData.objects.get(base_profile=53)
#     followers = 8
#     update_followers(profile_data, followers)
#     return HttpResponse("fireeeee")
#
# class ProfileListView(ListView):
#     pass
#
#
# class ProfileStatisticDetail(DetailView):
#     pass