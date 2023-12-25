from django.urls import path

from . import views
# from .views import index

urlpatterns = [
    path('profile_create/', views.BaseProfileCreateView.as_view(), name="profile_create"),
    path('profile_detail/<int:pk>/', views.BaseProfileDetailView.as_view(), name="profile_detail"),
    # path('profile_update/<int:profile_id>/', views.ProfileDinamicUpdateView.as_view(), name="profile_update")
    # path('profile_update/', index, name='profile_update')

]
