from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve
from django.http import FileResponse
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

def serve_geojson(request, filename):
    filepath = BASE / filename
    if filepath.exists() and filepath.suffix == '.geojson':
        return FileResponse(open(filepath, 'rb'), content_type='application/json')
    from django.http import Http404
    raise Http404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/tma/feed/', permanent=False)),
    path('', include('app.urls')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('geojson/<str:filename>', serve_geojson, name='geojson'),
]
