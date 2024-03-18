# Create your tasks here
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


@shared_task(bind=True)
def update_statistic(self):
    try:
        profiles = BaseProfile.objects.all()

        for profile in profiles:
            updater = ProfileStatsUpdater(profile.pk)
            updater.add_statistics()
            time.sleep(10)
            logger.info(f"Statistics updated for profile {updater.profile_data.name}.")
        # Логируем успешное обновление
        logger.info("Statistics successfully updated for all profiles.")
    except Exception as e:
        logger.error('Exceptional case, retry in 5 seconds.')
        raise self.retry(exc=e, countdown=5)
