from django.urls import path

from . import views


urlpatterns = [
    path('statistics/', views.BaseStatistic.as_view(), name="statistics"),

]
