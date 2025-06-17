from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from preLogin import models
from django.contrib.auth import views as auth_views

# Login
urlpatterns = [
    path('', views.login_view, name='login'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='preLogin/password_reset.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='preLogin/password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='preLogin/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='preLogin/password_reset_complete.html'), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)