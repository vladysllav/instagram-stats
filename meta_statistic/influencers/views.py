"""Views for the Influencers app."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import CreateView, DetailView

from default_auth.views import OwnProfileMixin
from .models import BaseProfile
from .forms import ProfileForm
from django.contrib.auth.models import User


class BaseProfileCreateView(LoginRequiredMixin, OwnProfileMixin, CreateView):
    """
    View for creating a new profile.
    """
    form_class = ProfileForm
    template_name = 'influencers/profile_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BaseProfileDetailView(LoginRequiredMixin, OwnProfileMixin, DetailView):
    """
    View for displaying a profile.
    """
    model = BaseProfile
    template_name = 'influencers/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds statistics data to the template context
        This method of expanding the basic context of the template for adding statistical data,
        associated with the object that will be added to the page.
        :param kwargs: Additional argument keywords that can be passed in the context.
        :return:  dict: Template context, additional data extensions.
        """
        context = super().get_context_data(**kwargs)
        context['statistics'] = self.object.statistics.first()
        return context
