from django.shortcuts import render
from django.db.models import Count
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Murojaat, MurojaatRasm, Statistika, Maktab, Vaada, Tekshiruv,
    VILOYATLAR, INFRATUZILMA_TURLARI,
)

# Viloyat markazlari koordinatalari
VILOYAT_COORDS = {
    'toshkent_sh':    {'lat': 41.2995, 'lng': 69.2401},
    'toshkent_v':     {'lat': 41.1173, 'lng': 69.7028},
    'samarqand':      {'lat': 39.6547, 'lng': 66.9758},
    'fargona':        {'lat': 40.3897, 'lng': 71.7857},
    'andijon':        {'lat': 40.8829, 'lng': 72.3234},
    'namangan':       {'lat': 41.0011, 'lng': 71.6726},
    'buxoro':         {'lat': 39.7747, 'lng': 64.4286},
    'xorazm':         {'lat': 41.5531, 'lng': 60.6325},
    'qashqadaryo':    {'lat': 38.8610, 'lng': 65.7870},
    'surxondaryo':    {'lat': 37.9404, 'lng': 67.5659},
    'jizzax':         {'lat': 40.1158, 'lng': 67.8422},
    'sirdaryo':       {'lat': 40.8363, 'lng': 68.6642},
    'navoiy':         {'lat': 40.1007, 'lng': 65.3791},
    'qoraqalpogiston':{'lat': 43.8006, 'lng': 59.0031},
}


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
        viloyat=viloyat,
        tuman=tuman,
        infratuzilma=infratuzilma,
        sektor=sektor,
        izoh=data.get('izoh', ''),
        telegram_user_id=int(telegram_user_id),
        telegram_username=data.get('telegram_username', ''),
        telegram_full_name=data.get('telegram_full_name', ''),
    )
    # Ko'p rasm saqlash
    rasmlar = request.FILES.getlist('rasmlar')
    if not rasmlar:
        single = request.FILES.get('rasm')
        if single:
            rasmlar = [single]
    for f in rasmlar:
        try:
            MurojaatRasm.objects.create(murojaat=murojaat, rasm=f)
        except Exception:
            pass  # Rasm saqlanmasa ham murojaat qabul qilinadi

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
    """Barcha maktablar ro'yxati + real-time statistika. ?viloyat=X&tuman=Y filter qilish mumkin"""
    maktablar = Maktab.objects.prefetch_related('tekshiruvlar', 'vaadalar').all()
    viloyat_filter = request.query_params.get('viloyat')
    tuman_filter = request.query_params.get('tuman')
    if viloyat_filter:
        maktablar = maktablar.filter(viloyat=viloyat_filter)
    if tuman_filter:
        maktablar = maktablar.filter(tuman=tuman_filter)
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


# ─── API: Viloyatlar (xarita uchun) ──────────────────────────────────────────

@api_view(['GET'])
def viloyatlar_api(request):
    """Har bir viloyat uchun maktab va va'da soni (xaritada bubble ko'rsatish)"""
    result = []
    for kod, nom in VILOYATLAR:
        coords = VILOYAT_COORDS.get(kod, {'lat': 41.2995, 'lng': 69.2401})
        maktablar = Maktab.objects.filter(viloyat=kod)
        if not maktablar.exists():
            continue
        maktab_ids = list(maktablar.values_list('id', flat=True))
        vaadalar_soni = Vaada.objects.filter(maktab_id__in=maktab_ids).count()
        result.append({
            'kod': kod,
            'nom': nom,
            'lat': coords['lat'],
            'lng': coords['lng'],
            'maktablar_soni': maktablar.count(),
            'vaadalar_soni': vaadalar_soni,
        })
    return Response(result)


@api_view(['POST'])
@parser_classes([JSONParser, FormParser])
def maktab_sync(request):
    """GEOASR dan kelgan maktabni lokal DB ga sinxronlash.
    Maktab yo'q bo'lsa yaratadi + standart va'dalar qo'shadi.
    Mavjud bo'lsa ID qaytaradi."""
    data = request.data
    obekt_nomi = data.get('obekt_nomi', '').strip()
    viloyat_nomi = data.get('viloyat', '').strip()
    tuman_nomi = data.get('tuman', '').strip()

    if not all([obekt_nomi, viloyat_nomi, tuman_nomi]):
        return Response({'error': 'obekt_nomi, viloyat, tuman majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    # GEOASR viloyat nomini lokal kodga aylantirish
    VILOYAT_NOM_TO_KOD = {
        "Qoraqolpog'iston Respublikasi": 'qoraqalpogiston',
        'Xorazm viloyati': 'xorazm',
        'Navoiy viloyati': 'navoiy',
        'Buxoro viloyati': 'buxoro',
        'Qashqadaryo viloyati': 'qashqadaryo',
        'Surxondaryo viloyati': 'surxondaryo',
        'Samarqand viloyati': 'samarqand',
        'Jizzax viloyati': 'jizzax',
        'Sirdaryo viloyati': 'sirdaryo',
        'Toshkent shahri': 'toshkent_sh',
        'Toshkent viloyati': 'toshkent_v',
        'Namangan viloyati': 'namangan',
        'Andijon viloyati': 'andijon',
        "Farg'ona viloyati": 'fargona',
    }
    viloyat_kod = VILOYAT_NOM_TO_KOD.get(viloyat_nomi, 'toshkent_sh')

    # Maktab mavjudligini tekshirish (nom + tuman bo'yicha)
    maktab = Maktab.objects.filter(nom=obekt_nomi, tuman=tuman_nomi).first()

    if not maktab:
        maktab = Maktab.objects.create(
            nom=obekt_nomi,
            viloyat=viloyat_kod,
            tuman=tuman_nomi,
            manzil=f"{tuman_nomi}, {viloyat_nomi}",
            rasm_url='',
        )
        # Standart va'dalar yaratish (GEOASR ma'lumotlariga asoslanib)
        standart_vaadalar = [
            {'nom': 'Ichimlik suvi', 'tavsif': "Maktabda toza ichimlik suvi ta'minoti", 'icon': 'water_drop', 'tartib': 1},
            {'nom': "Internet ta'minoti", 'tavsif': "Maktabda internet ulanishi holati", 'icon': 'wifi', 'tartib': 2},
            {'nom': 'Sport zal holati', 'tavsif': "Sport zal va sport jihozlari holati", 'icon': 'fitness_center', 'tartib': 3},
            {'nom': 'Oshxona holati', 'tavsif': "Maktab oshxonasi va ovqatlanish sifati", 'icon': 'restaurant', 'tartib': 4},
            {'nom': 'Hojatxona holati', 'tavsif': "Hojatxona tozaligi va ta'mirlanganligi", 'icon': 'wc', 'tartib': 5},
            {'nom': "Sovun ta'minoti", 'tavsif': "Hojatxonada sovun va gigiena vositalari", 'icon': 'soap', 'tartib': 6},
        ]
        for v in standart_vaadalar:
            Vaada.objects.create(maktab=maktab, **v)

    return Response({
        'success': True,
        'maktab_id': maktab.id,
        'nom': maktab.nom,
    })


@api_view(['GET'])
def tumanlari_api(request):
    """Berilgan viloyatdagi tumanlar va har birida nechta maktab/va'da bor"""
    viloyat = request.query_params.get('viloyat')
    if not viloyat:
        return Response({'error': 'viloyat parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

    tumanlari = (
        Maktab.objects.filter(viloyat=viloyat)
        .values('tuman')
        .annotate(maktablar_soni=Count('id'))
        .order_by('tuman')
    )

    result = []
    for t in tumanlari:
        maktab_ids = list(
            Maktab.objects.filter(viloyat=viloyat, tuman=t['tuman']).values_list('id', flat=True)
        )
        vaadalar_soni = Vaada.objects.filter(maktab_id__in=maktab_ids).count()
        result.append({
            'nom': t['tuman'],
            'maktablar_soni': t['maktablar_soni'],
            'vaadalar_soni': vaadalar_soni,
        })
    return Response(result)
