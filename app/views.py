from django.shortcuts import render
from django.db.models import Count
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Murojaat, Statistika, Maktab, Vaada, Tekshiruv,
    VILOYATLAR, INFRATUZILMA_TURLARI,
)


# ─── TMA sahifalari ──────────────────────────────────────────────────────────

def tma_dashboard(request):
    return render(request, 'index.html')

def tma_murojaat(request):
    return render(request, 'murojaat.html')

def tma_maktablar(request):
    return render(request, 'maktablar.html')

def tma_maktab_detail(request, maktab_id):
    return render(request, 'maktab_detail.html', {'maktab_id': maktab_id})

def tma_tahlil(request):
    return render(request, 'tahlil.html')


# ─── API: Statistika ─────────────────────────────────────────────────────────

@api_view(['GET'])
def statistika_api(request):
    stat = Statistika.objects.first()
    if not stat:
        stat = Statistika.objects.create()

    jami_tekshiruv = Tekshiruv.objects.count()
    bajarildi = Tekshiruv.objects.filter(natija='bajarildi').count()
    muammo = Tekshiruv.objects.filter(natija='muammo').count()
    mamnuniyat = round(bajarildi / jami_tekshiruv * 100) if jami_tekshiruv else 0

    return Response({
        'maktablar_soni': stat.maktablar_soni,
        'bogchalar_soni': stat.bogchalar_soni,
        'tibbiyot_soni': stat.tibbiyot_soni,
        'sport_soni': stat.sport_soni,
        'murojaatlar_soni': Murojaat.objects.count(),
        'hal_qilingan': Murojaat.objects.filter(holat='hal_qilindi').count(),
        'jami_tekshiruv': jami_tekshiruv,
        'bajarildi': bajarildi,
        'muammo': muammo,
        'mamnuniyat_foizi': mamnuniyat,
        'tekshirilgan_maktablar': Maktab.objects.filter(tekshiruvlar__isnull=False).distinct().count(),
    })


# ─── API: Murojaat ───────────────────────────────────────────────────────────

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def murojaat_yuborish(request):
    data = request.data
    telegram_user_id = data.get('telegram_user_id')
    if not telegram_user_id:
        return Response({'error': 'telegram_user_id majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    viloyat = data.get('viloyat', '').strip()
    tuman = data.get('tuman', '').strip()
    infratuzilma = data.get('infratuzilma', '').strip()
    sektor = data.get('sektor', '').strip()

    if not all([viloyat, tuman, infratuzilma, sektor]):
        return Response({'error': 'Viloyat, tuman, infratuzilma va sektor majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    murojaat = Murojaat.objects.create(
        rasm=data.get('rasm'),
        viloyat=viloyat,
        tuman=tuman,
        infratuzilma=infratuzilma,
        sektor=sektor,
        izoh=data.get('izoh', ''),
        telegram_user_id=int(telegram_user_id),
        telegram_username=data.get('telegram_username', ''),
        telegram_full_name=data.get('telegram_full_name', ''),
    )
    return Response({
        'success': True,
        'id': murojaat.id,
        'message': "Murojaatingiz qabul qilindi! 24 soat ichida ko'rib chiqiladi.",
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def murojaatlar_royxati(request):
    telegram_user_id = request.query_params.get('user_id')
    if not telegram_user_id:
        return Response({'error': 'user_id parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

    murojaatlar = Murojaat.objects.filter(telegram_user_id=int(telegram_user_id))
    data = [{
        'id': m.id,
        'viloyat': m.get_viloyat_display(),
        'tuman': m.tuman,
        'infratuzilma': m.get_infratuzilma_display(),
        'sektor': m.sektor,
        'izoh': m.izoh,
        'holat': m.get_holat_display(),
        'rasm': request.build_absolute_uri(m.rasm.url) if m.rasm else None,
        'yuborilgan_vaqt': m.yuborilgan_vaqt.strftime('%d.%m.%Y %H:%M'),
    } for m in murojaatlar]

    return Response({'murojaatlar': data, 'jami': len(data)})


# ─── API: Maktablar ──────────────────────────────────────────────────────────

@api_view(['GET'])
def maktablar_royxati(request):
    """Barcha maktablar ro'yxati + real-time statistika"""
    maktablar = Maktab.objects.prefetch_related('tekshiruvlar', 'vaadalar').all()
    data = []
    for m in maktablar:
        jami = Tekshiruv.objects.filter(maktab=m).count()
        bajarildi = Tekshiruv.objects.filter(maktab=m, natija='bajarildi').count()
        foiz = round(bajarildi / jami * 100) if jami else None

        if foiz is None:
            holat = 'tekshirilmagan'
            holat_rangi = '#94a3b8'
        elif foiz >= 70:
            holat = 'yaxshi'
            holat_rangi = '#22c55e'
        elif foiz >= 40:
            holat = "e'tiborga muhtoj"
            holat_rangi = '#f59e0b'
        else:
            holat = 'nosoz'
            holat_rangi = '#ef4444'

        data.append({
            'id': m.id,
            'nom': m.nom,
            'viloyat': m.get_viloyat_display(),
            'tuman': m.tuman,
            'manzil': m.manzil,
            'rasm_url': m.rasm_url,
            'lat': m.lat,
            'lng': m.lng,
            'jami_tekshiruv': jami,
            'bajarildi': bajarildi,
            'muammo': jami - bajarildi,
            'mamnuniyat_foizi': foiz,
            'holat': holat,
            'holat_rangi': holat_rangi,
            'vaadalar_soni': m.vaadalar.count(),
        })

    return Response({'maktablar': data, 'jami': len(data)})


@api_view(['GET'])
def maktab_detail_api(request, maktab_id):
    """Bitta maktab — vaadalar + tekshiruvlar statistikasi"""
    try:
        maktab = Maktab.objects.get(id=maktab_id)
    except Maktab.DoesNotExist:
        return Response({'error': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    vaadalar = []
    for v in maktab.vaadalar.all():
        jami = Tekshiruv.objects.filter(vaada=v).count()
        bajarildi = Tekshiruv.objects.filter(vaada=v, natija='bajarildi').count()
        muammo = jami - bajarildi
        foiz = round(bajarildi / jami * 100) if jami else None
        vaadalar.append({
            'id': v.id,
            'nom': v.nom,
            'tavsif': v.tavsif,
            'icon': v.icon,
            'jami': jami,
            'bajarildi': bajarildi,
            'muammo': muammo,
            'foiz': foiz,
        })

    so_nggi_tekshiruvlar = []
    for t in Tekshiruv.objects.filter(maktab=maktab).select_related('vaada')[:10]:
        so_nggi_tekshiruvlar.append({
            'id': t.id,
            'natija': t.natija,
            'natija_label': t.get_natija_display(),
            'vaada_nom': t.vaada.nom if t.vaada else '—',
            'izoh': t.izoh,
            'rasm': request.build_absolute_uri(t.rasm.url) if t.rasm else None,
            'fuqaro': t.telegram_full_name or f"Fuqaro #{t.telegram_user_id}",
            'vaqt': t.vaqt.strftime('%d.%m.%Y %H:%M'),
        })

    jami_t = Tekshiruv.objects.filter(maktab=maktab).count()
    bajarildi_t = Tekshiruv.objects.filter(maktab=maktab, natija='bajarildi').count()

    return Response({
        'id': maktab.id,
        'nom': maktab.nom,
        'viloyat': maktab.get_viloyat_display(),
        'tuman': maktab.tuman,
        'manzil': maktab.manzil,
        'rasm_url': maktab.rasm_url,
        'lat': maktab.lat,
        'lng': maktab.lng,
        'jami_tekshiruv': jami_t,
        'bajarildi': bajarildi_t,
        'muammo': jami_t - bajarildi_t,
        'mamnuniyat_foizi': round(bajarildi_t / jami_t * 100) if jami_t else None,
        'vaadalar': vaadalar,
        'so_nggi_tekshiruvlar': so_nggi_tekshiruvlar,
    })


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def tekshiruv_yuborish(request):
    """Fuqaro maktabdagi va'dani tekshiradi"""
    data = request.data
    telegram_user_id = data.get('telegram_user_id')
    maktab_id = data.get('maktab_id')
    natija = data.get('natija')

    if not all([telegram_user_id, maktab_id, natija]):
        return Response({'error': 'telegram_user_id, maktab_id, natija majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    if natija not in ('bajarildi', 'muammo'):
        return Response({'error': "natija: 'bajarildi' yoki 'muammo' bo'lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        maktab = Maktab.objects.get(id=int(maktab_id))
    except Maktab.DoesNotExist:
        return Response({'error': 'Maktab topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    vaada = None
    vaada_id = data.get('vaada_id')
    if vaada_id:
        try:
            vaada = Vaada.objects.get(id=int(vaada_id), maktab=maktab)
        except Vaada.DoesNotExist:
            pass

    tekshiruv = Tekshiruv.objects.create(
        maktab=maktab,
        vaada=vaada,
        natija=natija,
        rasm=data.get('rasm'),
        izoh=data.get('izoh', ''),
        telegram_user_id=int(telegram_user_id),
        telegram_username=data.get('telegram_username', ''),
        telegram_full_name=data.get('telegram_full_name', ''),
    )

    # Maktab holatini yangilash
    jami = Tekshiruv.objects.filter(maktab=maktab).count()
    bajarildi_soni = Tekshiruv.objects.filter(maktab=maktab, natija='bajarildi').count()
    foiz = round(bajarildi_soni / jami * 100) if jami else 0
    if foiz >= 70:
        maktab.holat = 'yaxshi'
    elif foiz >= 40:
        maktab.holat = 'etiborga_muhtoj'
    else:
        maktab.holat = 'nosoz'
    maktab.save(update_fields=['holat'])

    return Response({
        'success': True,
        'id': tekshiruv.id,
        'mamnuniyat_foizi': foiz,
        'message': "Tekshiruvingiz qabul qilindi! Rahmat.",
    }, status=status.HTTP_201_CREATED)


# ─── API: Tahlil (Solishtirma) ────────────────────────────────────────────────

@api_view(['GET'])
def tahlil_api(request):
    """Solishtirma tahlil uchun umumlashtirilgan ma'lumotlar"""

    # 1. Viloyatlar bo'yicha mamnuniyat
    viloyatlar_tahlil = []
    for kod, nom in VILOYATLAR:
        maktablar = Maktab.objects.filter(viloyat=kod)
        if not maktablar.exists():
            continue
        maktab_ids = list(maktablar.values_list('id', flat=True))
        jami = Tekshiruv.objects.filter(maktab_id__in=maktab_ids).count()
        bajarildi = Tekshiruv.objects.filter(maktab_id__in=maktab_ids, natija='bajarildi').count()
        foiz = round(bajarildi / jami * 100) if jami else 0
        viloyatlar_tahlil.append({
            'viloyat': nom,
            'maktablar_soni': maktablar.count(),
            'jami_tekshiruv': jami,
            'bajarildi': bajarildi,
            'muammo': jami - bajarildi,
            'mamnuniyat_foizi': foiz,
        })

    # 2. Muammo turlari (va'dalar bo'yicha)
    muammo_turlari = (
        Tekshiruv.objects
        .filter(natija='muammo', vaada__isnull=False)
        .values('vaada__nom')
        .annotate(soni=Count('id'))
        .order_by('-soni')[:8]
    )

    # 3. Top 5 maktab — eng yaxshi va eng yomon
    maktablar = Maktab.objects.all()
    maktab_reytingi = []
    for m in maktablar:
        jami = Tekshiruv.objects.filter(maktab=m).count()
        if jami == 0:
            continue
        bajarildi = Tekshiruv.objects.filter(maktab=m, natija='bajarildi').count()
        foiz = round(bajarildi / jami * 100)
        maktab_reytingi.append({
            'id': m.id,
            'nom': m.nom,
            'viloyat': m.get_viloyat_display(),
            'tuman': m.tuman,
            'mamnuniyat_foizi': foiz,
            'jami_tekshiruv': jami,
        })

    maktab_reytingi.sort(key=lambda x: x['mamnuniyat_foizi'], reverse=True)

    # 4. Umumiy ko'rsatkichlar
    jami_t = Tekshiruv.objects.count()
    baj_t = Tekshiruv.objects.filter(natija='bajarildi').count()
    mum_t = jami_t - baj_t

    return Response({
        'viloyatlar': viloyatlar_tahlil,
        'muammo_turlari': [
            {'nom': item['vaada__nom'], 'soni': item['soni']}
            for item in muammo_turlari
        ],
        'eng_yaxshi_maktablar': maktab_reytingi[:5],
        'eng_yomon_maktablar': list(reversed(maktab_reytingi[-5:])),
        'umumiy': {
            'jami_tekshiruv': jami_t,
            'bajarildi': baj_t,
            'muammo': mum_t,
            'mamnuniyat_foizi': round(baj_t / jami_t * 100) if jami_t else 0,
            'tekshirilgan_maktablar': len(maktab_reytingi),
        },
    })


@api_view(['GET'])
def meta_api(request):
    return Response({
        'viloyatlar': [{'value': v[0], 'label': v[1]} for v in VILOYATLAR],
        'infratuzilma_turlari': [{'value': i[0], 'label': i[1]} for i in INFRATUZILMA_TURLARI],
    })
