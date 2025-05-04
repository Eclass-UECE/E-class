from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscricao_view, name='inscricao'),
    path('anexos/<str:inscricao_id>/', views.anexos_view, name='anexos'),
    path('sucesso/<str:inscricao_id>/', views.sucesso_view, name='pagina_de_sucesso'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)