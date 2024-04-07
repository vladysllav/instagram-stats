from datetime import datetime, timedelta

from django.db.models import F, OuterRef, Subquery
from django.utils import timezone


class InfluencersStatisticsServices:

    def __init__(self, current_user):
        self.current_user = current_user

    def process_statistics(self, date_start, date_end):
        return self._get_queryset_with_profiles(date_start, date_end)

    def _get_queryset_with_profiles(self, date_start, date_end):
        """
        Отримує queryset з профілями для обчислення зміни кількості фоловерів та відсоткової зміни за період.
        """
        from influencers_statistic.models import Statistics  # для уникнення циклічного імпорта

        current_date = timezone.now().date()
        if date_end > current_date:
            return None
        else:
            end_followers_subquery = Statistics.objects.filter(
                profile__user=self.current_user,
                created_at__date=date_end,
                profile=OuterRef("profile"),  # фільтр по профілю
            ).values("followers")[
                :1
            ]  # вибір останнього значення

            queryset = Statistics.objects.filter(
                profile__user=self.current_user,
                created_at__date__gte=date_start,
                created_at__date__lte=date_end,
            ).annotate(
                end_followers_number=Subquery(end_followers_subquery),
                followers_change_number=F("end_followers_number") - F("followers"),
                followers_change_percent=(F("followers_change_number") * 100.0) / F("followers"),
            )

            return self._order_queryset_by_end_followers_count(queryset)

    @staticmethod
    def _order_queryset_by_end_followers_count(queryset):
        """Повертає відсортований queryset з унікальними значеннями за датою створення"""
        return queryset.order_by("created_at").distinct()

    @staticmethod
    def validate_dates(date_start, date_end):

        from influencers_statistic.models import Statistics  # для уникнення циклічного імпорта

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
