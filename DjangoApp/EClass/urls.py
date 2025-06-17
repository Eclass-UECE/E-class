from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('preLogin.urls')),  # Se o preLogin é responsável pela página inicial
    path('login/', include('login.urls')),
    path('admin/', admin.site.urls),
    path('', include("preLogin.urls")),
    path('pagProf/', include("posLogin.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

