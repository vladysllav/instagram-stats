from datetime import datetime, timedelta

from django.utils import timezone
from influencers_statistic.models import Statistics


class InfluencersStatisticsServices:

    @staticmethod
    def validate_dates(date_start, date_end):

        if date_start and date_end:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
            date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
            if date_start > date_end:
                return Statistics.objects.none()
        else:
            current_date = timezone.now().date()
            date_start = current_date - timedelta(days=30)
            date_end = current_date

        return date_start, date_end
