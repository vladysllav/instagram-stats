"""Signals for influencers app."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import client


@receiver(post_save, sender="influencers.BaseProfile")
def create_dynamic_profile_data(sender, instance, created, **kwargs):
    """
    Creates a Statistics object when a new BaseProfile is created.
    This post_save signal handler automatically creates an entry in the Statistics model,
    when a new BaseProfile instance is created. It uses functions
    for additional profile information, such as profile photo URL,
    number of subscribers, etc.
    :param sender: The model class that sent the signal.
    :param instance: The instance of the model that was saved.
    :param created: Whether a new instance was created (True if so).
    :param kwargs: Additional keyword arguments.
    :return:
    """

    from influencers_statistic.models import Statistics

    if created:
        url_profile = instance.url_profile
        name = url_profile.rstrip("/").split("/")[-1]
        Statistics.objects.create(
            profile=instance,
            name=name,
            profile_pictures=client.get_save_profile_pictures(name),
            followers=client.get_profile_followers(name),
            profile_pictures_url=client.get_profile_photo(name),
        )
