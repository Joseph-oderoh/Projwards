from . import views
from django.urls import path, re_path

urlpatterns = [
    path('search/', views.search_results, name='search_results'),
    path('', views.homepage, name='landing'),
    path('profile/<username>/', views.profile, name='profile'),
    path('<username>/profile', views.user_profile, name='userprofile'),
    path('profile/<username>/settings', views.edit_profile, name='edit'),
    path('projectdetails/<project_id>',views.project_details,name='projectdetails'),
    path('rates/<project_id>',views.submit_rates,name='submitrates'),
    path('user/add/project', views.add_project, name='addproject'),
    path('api/project/', views.ProjectList.as_view(),name=''),
    path('api/profile/', views.ProfileList.as_view(),name='')
]