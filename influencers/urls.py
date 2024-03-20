"""URLs for the influencers app."""

from django.urls import path

from . import views


urlpatterns = [
    path("profiles/", views.BaseProfileCreateView.as_view(), name="profile_create"),
    path("profiles/<int:pk>/", views.BaseProfileDetailView.as_view(), name="profile_detail"),
    # path('profile_update/<int:profile_id>/', views.ProfileDinamicUpdateView.as_view(), name="profile_update")
    # path('profile_update/', index, name='profile_update')
]
