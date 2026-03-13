from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/tma/', permanent=False)),
    path('', include('app.urls')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
