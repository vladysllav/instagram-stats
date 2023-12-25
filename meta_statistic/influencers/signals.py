
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import get_profile_photo, get_profile_followers, get_save_profile_pictures
# from influencers_statistic.models import Statistics
#
@receiver(post_save, sender='influencers.BaseProfile')
def create_dynamic_profile_data(sender, instance, created, **kwargs):
    # from influencers.models import BaseProfile  # Перенесен импорт внутрь функции
    from influencers_statistic.models import Statistics  # Перенесен импорт внутрь функции

    if created:
        url_profile = instance.url_profile
        name = url_profile.rstrip('/').split('/')[-1]
        Statistics.objects.create(
            profile=instance,
            name=name,
            profile_pictures=get_save_profile_pictures(name),
            followers=get_profile_followers(name),
        )

        # user_data, _ = UserData.objects.get_or_create(user=instance)
        # user_data.name = name
        # user_data.profile_pictures = get_save_profile_pictures(name)
        # user_data.followers = get_profile_followers(name)
        # user_data.save()