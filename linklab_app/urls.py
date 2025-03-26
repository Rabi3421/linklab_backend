from django.contrib import admin
from django.urls import path
from linklab_app import views

urlpatterns = [
    path('hello/', views.hello_django, name='hello_django'),
    path('social_media_login/', views.social_media_login_views, name='social_media_login'),
    path('profile/', views.get_user_info, name='profile'),
    path('update_profile/', views.update_user_info_views, name='update_profile'),
    path('logout/', views.user_logout_view, name="logout"),
    # linklab short url functionality
    path('shorten_url/crud/', views.create_short_url_views, name='shorten_url'),
    path('<str:short_code>', views.redirect_to_original, name='redirect'),
    path('get_tracking/', views.get_tracking_views, name='get_shortened_url'),
]
