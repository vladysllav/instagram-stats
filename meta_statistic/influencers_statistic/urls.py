from django.urls import path

from . import views
from .views import update_statistic

urlpatterns = [
    path('statistics/', views.BaseStatistic.as_view(), name="statistics"),
    path('statistics_update/', update_statistic, name='statistics_update'),
    path('statistics_table/', views.UserProfileView.as_view(), name="statistics_table"),

]
