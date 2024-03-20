from django.urls import path

from . import views
from .views import update_statistic_view

urlpatterns = [
    path('statistics/', views.BaseStatistic.as_view(), name="statistics"),
    path('statistics_update/', update_statistic_view, name='statistics_update'),
    path('period_statistics', views.PeriodStatistic.as_view(), name="period_statistics"),
    # path('statistics_table/', views.StatisticsListView.as_view(), name="statistics_table"),

]
