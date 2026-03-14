from django.urls import path
from . import views

urlpatterns = [
    # ── TMA sahifalari ──────────────────────────────────────────
    path('tma/', views.tma_dashboard, name='tma_dashboard'),
    path('tma/murojaat/', views.tma_murojaat, name='tma_murojaat'),
    path('tma/maktablar/', views.tma_maktablar, name='tma_maktablar'),
    path('tma/maktablar/<int:maktab_id>/', views.tma_maktab_detail, name='tma_maktab_detail'),
    path('tma/tahlil/', views.tma_tahlil, name='tma_tahlil'),

    # ── REST API ────────────────────────────────────────────────
    path('api/statistika/', views.statistika_api, name='api_statistika'),
    path('api/murojaat/', views.murojaat_yuborish, name='api_murojaat'),
    path('api/murojaatlar/', views.murojaatlar_royxati, name='api_murojaatlar'),
    path('api/maktablar/', views.maktablar_royxati, name='api_maktablar'),
    path('api/maktablar/<int:maktab_id>/', views.maktab_detail_api, name='api_maktab_detail'),
    path('api/tekshiruv/', views.tekshiruv_yuborish, name='api_tekshiruv'),
    path('api/maktab-sync/', views.maktab_sync, name='api_maktab_sync'),
    path('api/tahlil/', views.tahlil_api, name='api_tahlil'),
    path('api/meta/', views.meta_api, name='api_meta'),
    path('api/viloyatlar/', views.viloyatlar_api, name='api_viloyatlar'),
    path('api/tumanlari/', views.tumanlari_api, name='api_tumanlari'),
]
