from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('', views.pagInicial, name='pagInicial'),
    path('inscricao/', views.inscricao_view, name='inscricao'),
    path('anexos/<str:inscricao_id>/', views.anexos_view, name='anexos'),
    path('sucesso/<str:inscricao_id>/', views.sucesso_view, name='pagina_de_sucesso'),
    path('coordenador/', views.coordenador_view, name='coordenador'),
    path('testeNivel/<str:inscricao_id>/', views.testeNivel_view, name='testeNivel'),
    path('responde_ia/', views.responde_ia, name='responde_ia')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
