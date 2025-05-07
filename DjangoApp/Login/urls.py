from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from preLogin import models
from django.contrib.auth import views as auth_views

# Login
urlpatterns = [
    path('', views.login_view, name='login'),

    # URL para solicitar a redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    # URL para o envio do e-mail com o link de redefinição de senha
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # URL para o link de redefinição de senha enviado por e-mail
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # URL após a redefinição bem-sucedida
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)