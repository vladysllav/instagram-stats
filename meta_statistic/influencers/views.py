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

