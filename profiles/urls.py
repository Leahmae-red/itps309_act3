# profiles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile_home'),
    path('user/<str:username>/', views.profile_view, name='profile_detail'),
    path('api/update-avatar/', views.update_avatar_ajax, name='update_avatar_ajax'),
    path('api/update-cover/', views.update_cover_ajax, name='update_cover_ajax'),
    path('api/update-bio/', views.update_bio_ajax, name='update_bio_ajax'),
    path('api/like/<int:post_id>/', views.toggle_like_ajax, name='toggle_like_ajax'),
]