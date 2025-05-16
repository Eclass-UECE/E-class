from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('', views.pagInicial, name='pagInicial'),
    path('login/', include('Login.urls')),
    path('inscricao/', views.inscricao_view, name='inscricao'),
    path('anexos/<str:inscricao_id>/', views.anexos_view, name='anexos'),
    path('sucesso/<str:inscricao_id>/', views.sucesso_view, name='pagina_de_sucesso'),
    path('egresso/', views.egresso, name='egresso'),
    path('testeNivel/', views.testeNivel, name='testeNivel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)