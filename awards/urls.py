from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.homepage, name='landing'),
    path('profile/<username>/', views.profile, name='profile'),
    path('<username>/profile', views.user_profile, name='userprofile'),
]