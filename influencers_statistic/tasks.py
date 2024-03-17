# Create your tasks here
import random
import time

from celery import shared_task
from django.http import HttpResponse

from influencers.models import BaseProfile
from influencers_statistic.views import ProfileStatsUpdater
import logging

# @shared_task
# def add():
#     print("start stask")
#     return f"hello world"

logger = logging.getLogger(__name__)


@shared_task
def update_statistic():
    profiles = BaseProfile.objects.all()
    for profile in profiles:
        updater = ProfileStatsUpdater(profile.pk)
        updater.add_statistics()
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)
        logger.info(f"Statistics updated for profile {updater.profile_data.name}.")
    # Логируем успешное обновление
    logger.info("Statistics successfully updated for all profiles.")
