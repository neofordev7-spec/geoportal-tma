"""
Namunaviy ma'lumotlar: 10 ta maktab, har birida 3-4 va'da,
va demo tekshiruvlar (Zarina va boshqa fuqarolar tomonidan).

Ishga tushirish:
    python manage.py seed_data
"""
import random
from django.core.management.base import BaseCommand
from app.models import Maktab, Vaada, Tekshiruv, Statistika, Murojaat, MurojaatRasm, Like, Comment


MAKTABLAR = [
    {
        'nom': '45-sonli umumta\'lim maktabi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Yunusobod tumani',
        'manzil': 'Yunusobod tumani, Amir Temur ko\'chasi 12',
        'rasm_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/School_in_Tashkent.jpg/640px-School_in_Tashkent.jpg',
        'lat': 41.3312, 'lng': 69.2876,
        'vaadalar': [
            {'nom': 'Hojatxonalarni ta\'mirlash', 'tavsif': 'Bolalar va o\'qituvchilar hojatxonasi ta\'mirlanishi kerak edi', 'icon': 'plumbing'},
            {'nom': 'Sovun idishlarini o\'rnatish', 'tavsif': 'Barcha sinfxonalar va hojatxonalarga sovun dispenser o\'rnatilishi', 'icon': 'soap'},
            {'nom': 'Yangi o\'quv partalar', 'tavsif': '1-4 sinf o\'quvchilari uchun 120 ta yangi parta va stul', 'icon': 'chair'},
            {'nom': 'Devorlarni bo\'yash', 'tavsif': 'Koridor va sinfxona devorlarini yangilash', 'icon': 'format_paint'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Hojatxonalar ta\'mirlandi, zo\'r!', 1),
            ('bajarildi', 'Sovun idishlari bor, ishlayapti', 2),
            ('muammo', 'Partalarning yarmi hali kelmadi', 3),
            ('bajarildi', 'Devorlar bo\'yaldi', 1),
            ('muammo', 'Bir nechta sovun idishi singan', 4),
        ]
    },
    {
        'nom': '78-sonli umumta\'lim maktabi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Chilonzor tumani',
        'manzil': 'Chilonzor tumani, Bunyodkor ko\'chasi 34',
        'rasm_url': '',
        'lat': 41.2845, 'lng': 69.1976,
        'vaadalar': [
            {'nom': 'Internet aloqasini yaxshilash', 'tavsif': 'Optik tolali internet va Wi-Fi nuqtalarini o\'rnatish', 'icon': 'wifi'},
            {'nom': 'Maktab kutubxonasini yangilash', 'tavsif': '500 ta yangi darslik va qo\'shimcha adabiyotlar', 'icon': 'library_books'},
            {'nom': 'Sport maydonini ta\'mirlash', 'tavsif': 'Futbol maydoni va basketbol to\'plarini yangilash', 'icon': 'sports_soccer'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Internet tezkor ishlayapti!', 5),
            ('bajarildi', 'Kutubxona yangilandi', 6),
            ('muammo', 'Sport maydoni hali ta\'mirlanmadi', 5),
            ('muammo', 'Wi-Fi 2-qavatda ishlamaydi', 7),
        ]
    },
    {
        'nom': '12-sonli umumta\'lim maktabi',
        'viloyat': 'samarqand',
        'tuman': 'Samarqand shahri',
        'manzil': 'Samarqand shahri, Registon ko\'chasi 5',
        'rasm_url': '',
        'lat': 39.6542, 'lng': 66.9597,
        'vaadalar': [
            {'nom': 'Sinf xonalarini ta\'mirlash', 'tavsif': '12 ta sinf xonasida derazalar va eshiklarni almashtirish', 'icon': 'window'},
            {'nom': 'Suv ta\'minotini yaxshilash', 'tavsif': 'Ichimlik suvi quvurlari va filtrlash tizimini yangilash', 'icon': 'water_drop'},
            {'nom': 'Isitish tizimini ta\'mirlash', 'tavsif': 'Qish fasli uchun kalorifer tizimini yangilash', 'icon': 'local_fire_department'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Derazalar almashtirildi', 8),
            ('bajarildi', 'Suv toza va bosim yaxshi', 9),
            ('bajarildi', 'Isitish tizimi ishlayapti', 8),
            ('bajarildi', 'Hammasi zo\'r!', 10),
            ('bajarildi', 'Yaxshi ishlashdi', 11),
        ]
    },
    {
        'nom': '33-sonli umumta\'lim maktabi',
        'viloyat': 'fargona',
        'tuman': "Farg'ona shahri",
        'manzil': "Farg'ona shahri, Mustaqillik ko'chasi 17",
        'rasm_url': '',
        'lat': 40.3842, 'lng': 71.7843,
        'vaadalar': [
            {'nom': 'Boshlang\'ich sinf xonalarini ta\'mirlash', 'tavsif': '1-4 sinf xonalarini to\'liq ta\'mirlash', 'icon': 'construction'},
            {'nom': 'Kompyuter xonasini yangilash', 'tavsif': '20 ta yangi kompyuter o\'rnatish', 'icon': 'computer'},
            {'nom': 'Maktab hovlisini obodonlashtirish', 'tavsif': 'Daraxtlar ekish va yo\'lka qilish', 'icon': 'park'},
        ],
        'tekshiruvlar': [
            ('muammo', 'Boshlang\'ich sinf xonalari hali ta\'mirlanmadi', 12),
            ('muammo', 'Kompyuterlar hali kelmadi', 13),
            ('muammo', 'Hovli ham o\'zgarmadi', 12),
        ]
    },
    {
        'nom': '55-sonli umumta\'lim maktabi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Mirobod tumani',
        'manzil': 'Mirobod tumani, Shota Rustaveli ko\'chasi 8',
        'rasm_url': '',
        'lat': 41.3052, 'lng': 69.2831,
        'vaadalar': [
            {'nom': 'Yangi qo\'shimcha bino qurilishi', 'tavsif': '8 ta yangi sinf xonasi uchun 2-qavatli bino', 'icon': 'apartment'},
            {'nom': 'Xavfsizlik kameralari o\'rnatish', 'tavsif': 'Maktab hududida 12 ta kamera', 'icon': 'videocam'},
            {'nom': 'Maktab oshxonasini ta\'mirlash', 'tavsif': 'Yangi uskunalar va sanitariya', 'icon': 'restaurant'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Yangi bino qurilmoqda, progress bor', 14),
            ('bajarildi', 'Kameralar o\'rnatildi', 15),
            ('muammo', 'Oshxona hali ta\'mirlanmagan', 14),
            ('bajarildi', 'Bino deyarli tayyor', 16),
        ]
    },
    {
        'nom': '91-sonli umumta\'lim maktabi',
        'viloyat': 'andijon',
        'tuman': 'Andijon shahri',
        'manzil': 'Andijon shahri, Navoiy ko\'chasi 22',
        'rasm_url': '',
        'lat': 40.7821, 'lng': 72.3442,
        'vaadalar': [
            {'nom': 'Hojatxonalarni ta\'mirlash', 'tavsif': 'O\'g\'il bolalar va qizlar hojatxonasini yangilash', 'icon': 'plumbing'},
            {'nom': 'Yangi o\'quv qurollari', 'tavsif': 'Laboratoriya jihozlari va sport inventarlar', 'icon': 'science'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Hojatxona ta\'mirlandi', 17),
            ('muammo', 'Laboratoriya jihozlari kelmadi', 18),
            ('bajarildi', 'Yaxshi', 19),
        ]
    },
    {
        'nom': '17-sonli umumta\'lim maktabi',
        'viloyat': 'namangan',
        'tuman': 'Namangan shahri',
        'manzil': 'Namangan shahri, Istiqlol ko\'chasi 45',
        'rasm_url': '',
        'lat': 40.9983, 'lng': 71.6726,
        'vaadalar': [
            {'nom': 'Energiya tejovchi chiroqlar', 'tavsif': 'LED chiroqlar bilan almashtirish', 'icon': 'lightbulb'},
            {'nom': 'Maktab bog\'ini yangilash', 'tavsif': 'Yangi o\'simliklar va dam olish joylari', 'icon': 'nature'},
            {'nom': 'Ta\'lim texnologiyalari', 'tavsif': 'Interaktiv doskalar o\'rnatish', 'icon': 'cast_for_education'},
        ],
        'tekshiruvlar': []
    },
    {
        'nom': '62-sonli umumta\'lim maktabi',
        'viloyat': 'buxoro',
        'tuman': 'Buxoro shahri',
        'manzil': 'Buxoro shahri, Hamza ko\'chasi 3',
        'rasm_url': '',
        'lat': 39.7747, 'lng': 64.4286,
        'vaadalar': [
            {'nom': 'Yangi o\'quv partalar', 'tavsif': '200 ta yangi parta va stul', 'icon': 'chair'},
            {'nom': 'Hovli asfaltlash', 'tavsif': 'Maktab hovlisini asfalt qilish', 'icon': 'road'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Partalar keldi!', 20),
            ('bajarildi', 'Asphalt qilindi', 21),
            ('bajarildi', 'Hammasi yaxshi', 20),
        ]
    },
    {
        'nom': '28-sonli umumta\'lim maktabi',
        'viloyat': 'qashqadaryo',
        'tuman': 'Qarshi shahri',
        'manzil': 'Qarshi shahri, Beruniy ko\'chasi 11',
        'rasm_url': '',
        'lat': 38.8601, 'lng': 65.7911,
        'vaadalar': [
            {'nom': 'Xavfsizlik qo\'riqxonasi', 'tavsif': 'Maktab kirishida qo\'riq post', 'icon': 'security'},
            {'nom': 'Favqulodda chiqish joylari', 'tavsif': 'Yong\'in qochish yo\'llarini belgilash', 'icon': 'emergency_exit'},
            {'nom': 'Tibbiy xona jihozlash', 'tavsif': 'Birinchi yordam anjomlarini to\'ldirish', 'icon': 'medical_services'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Qo\'riq post bor', 22),
            ('muammo', 'Favqulodda chiqishlar belgilanmagan', 22),
            ('bajarildi', 'Tibbiy xona to\'ldirildi', 23),
            ('muammo', 'Bir eshik bloklanib qolgan', 24),
        ]
    },
    {
        'nom': '44-sonli umumta\'lim maktabi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Shayxontohur tumani',
        'manzil': 'Shayxontohur tumani, Abdulla Qodiriy ko\'chasi 7',
        'rasm_url': '',
        'lat': 41.3205, 'lng': 69.2401,
        'vaadalar': [
            {'nom': 'Yangi futbol maydoni', 'tavsif': 'Suniy o\'t bilan qoplangan futbol maydoni', 'icon': 'sports_soccer'},
            {'nom': 'Maktab uniformasi', 'tavsif': '1-sinf o\'quvchilari uchun bepul forma', 'icon': 'checkroom'},
            {'nom': 'Raqamli kutubxona', 'tavsif': 'Elektron kitoblar va planshets', 'icon': 'tablet_android'},
        ],
        'tekshiruvlar': [
            ('bajarildi', 'Futbol maydoni zo\'r!', 25),
            ('bajarildi', 'Formalar berildi', 26),
            ('muammo', 'Planshetslar kelmadi', 25),
            ('bajarildi', 'Maydonda o\'ynaymiz', 27),
            ('bajarildi', 'Formalar ajoyib', 28),
        ]
    },
]


class Command(BaseCommand):
    help = "Namunaviy maktablar, va'dalar va tekshiruvlar ma'lumotlarini yaratish"

    def handle(self, *args, **kwargs):
        self.stdout.write("Ma'lumotlar yuklanmoqda...")

        # Statistika yaratish
        if not Statistika.objects.exists():
            Statistika.objects.create()
            self.stdout.write(self.style.SUCCESS("✓ Statistika yaratildi"))

        created = 0
        for data in MAKTABLAR:
            maktab, new = Maktab.objects.get_or_create(
                nom=data['nom'],
                defaults={
                    'viloyat': data['viloyat'],
                    'tuman': data['tuman'],
                    'manzil': data['manzil'],
                    'rasm_url': data['rasm_url'],
                    'lat': data['lat'],
                    'lng': data['lng'],
                }
            )
            if not new:
                continue

            # Va'dalar yaratish
            for i, v in enumerate(data['vaadalar']):
                vaada = Vaada.objects.create(
                    maktab=maktab,
                    nom=v['nom'],
                    tavsif=v['tavsif'],
                    icon=v['icon'],
                    tartib=i,
                )

                # Har bir va'da uchun tegishli demo tekshiruvlar
                for natija, izoh, user_id in data['tekshiruvlar']:
                    if random.random() > 0.4:
                        Tekshiruv.objects.create(
                            maktab=maktab,
                            vaada=vaada,
                            natija=natija,
                            izoh=izoh,
                            telegram_user_id=1000000 + user_id,
                            telegram_username=f'fuqaro_{user_id}',
                            telegram_full_name=random.choice([
                                'Zarina Yusupova', 'Alisher Karimov', 'Malika Tosheva',
                                'Bobur Rahimov', 'Nilufar Hasanova', 'Jasur Umarov',
                                'Dilnoza Ergasheva', 'Sherzod Mirzayev'
                            ]),
                        )

            # Maktab holatini yangilash
            jami = Tekshiruv.objects.filter(maktab=maktab).count()
            if jami > 0:
                baj = Tekshiruv.objects.filter(maktab=maktab, natija='bajarildi').count()
                foiz = round(baj / jami * 100)
                maktab.holat = 'yaxshi' if foiz >= 70 else 'etiborga_muhtoj' if foiz >= 40 else 'nosoz'
                maktab.save(update_fields=['holat'])

            created += 1
            self.stdout.write(f"  ✓ {maktab.nom}")

        if created:
            self.stdout.write(self.style.SUCCESS(f"\n{created} ta maktab muvaffaqiyatli yaratildi!"))
        else:
            self.stdout.write(self.style.WARNING("Ma'lumotlar allaqachon mavjud."))

        jami_t = Tekshiruv.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Jami tekshiruvlar: {jami_t} ta"))

        # ── Lenta postlari ──────────────────────────────────────
        self.stdout.write("\nLenta postlari yuklanmoqda...")
        LENTA_POSTS = [
            {
                'izoh': "Qarshi–Shahrisabz magistral yo'li ta'miri nega to'xtab qoldi?\n\nQarshi–Shahrisabz magistral avtomobil yo'lining Yakkabog' tumanidan o'tgan qismida olib borilayotgan ta'mirlash ishlari o'tgan yil dekabr oyidan beri to'xtab qolgan.",
                'viloyat': 'qashqadaryo',
                'tuman': 'Yakkabog\'',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000001,
                'telegram_full_name': 'Dilshod Rahmatov',
                'is_anonim': False,
                'holat': 'kutilmoqda',
                'media': ['/static/lenta/qarshi_yakkaboq.mp4'],
                'likes': 47,
                'comments': [
                    ('Jasur Toshev', "Bu yo'ldan har kuni o'taman, juda xavfli holatda!"),
                    ('Nilufar K.', "O'tgan yili ham shunday edi, va'da berishdi lekin hech narsa qilishmadi"),
                    ('Sardor M.', "Hokimlikka murojaatlar yubordik, javob yo'q"),
                    ('Zulfiya A.', "Yomg'ir yog'sa loy bo'lib ketadi, mashinalar buziladi"),
                ],
            },
            {
                'izoh': "Asfalt yo'limiz qurib berildi, juda xursandmiz! Rahmat hukumatga!",
                'viloyat': 'qashqadaryo',
                'tuman': 'Qarshi shahri',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000002,
                'telegram_full_name': 'Malika Yusupova',
                'is_anonim': False,
                'holat': 'hal_qilindi',
                'media': ['/static/lenta/asfalt.mp4'],
                'likes': 124,
                'comments': [
                    ('Bobur R.', "Bizning mahallaga ham shunaqa qilishsa!"),
                    ('Aziza T.', "Zo'r! Axir bajarildi!"),
                    ('Otabek N.', "Qancha vaqt davom etdi ta'mir?"),
                    ('Shahlo I.', "Hammaga nasib qilsin!"),
                    ('Kamol D.', "Qo'shnilarimiz ham xursand"),
                ],
            },
            {
                'izoh': "Va'dalar beriladi, muammo esa echilmaydi: Guliston mahallasining chang va loy ko'chasi qachondir ta'mirlanadimi?\n\nQashqadaryo viloyati Qarshi tumanidagi Guliston mahallasi aholisi tuman hokimligi tomonidan yillar davomida berilayotgan va'dalar bajarilmayotgani yuzasidan murojaat yo'lladi.",
                'viloyat': 'qashqadaryo',
                'tuman': 'Qarshi tumani',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000003,
                'telegram_full_name': 'Anonim fuqaro',
                'is_anonim': True,
                'holat': 'kutilmoqda',
                'media': ['/static/lenta/kocha.jpg', '/static/lenta/kocha3.jpg', '/static/lenta/kochaq.jpg'],
                'likes': 89,
                'comments': [
                    ('Zarina Y.', "Bizning mahallada ham xuddi shunday ahvol"),
                    ('Alisher K.', "5 yildan beri va'da berishyapti!"),
                    ('Dilnoza E.', "Bolalar maktabga loy ichida borishyapti, uyat!"),
                    ('Sherzod M.', "Buni televideniyega chiqarish kerak"),
                    ('Nodira H.', "Hokimga yozing, telegram kanalga ham tashlang"),
                    ('Jasur U.', "Hammamiz birgalikda ovoz ko'tarishimiz kerak"),
                ],
            },
        ]

        if Murojaat.objects.filter(telegram_user_id__gte=2000001, telegram_user_id__lte=2000003).exists():
            self.stdout.write(self.style.WARNING("Lenta postlari allaqachon mavjud."))
        else:
            for post_data in LENTA_POSTS:
                murojaat = Murojaat.objects.create(
                    izoh=post_data['izoh'],
                    viloyat=post_data['viloyat'],
                    tuman=post_data['tuman'],
                    infratuzilma=post_data['infratuzilma'],
                    sektor='',
                    telegram_user_id=post_data['telegram_user_id'],
                    telegram_full_name=post_data['telegram_full_name'],
                    is_anonim=post_data['is_anonim'],
                    holat=post_data['holat'],
                )
                # Media fayllar
                for media_path in post_data['media']:
                    MurojaatRasm.objects.create(murojaat=murojaat, rasm=media_path)

                # Likelar
                for i in range(post_data['likes']):
                    Like.objects.create(
                        murojaat=murojaat,
                        telegram_user_id=3000000 + i,
                    )

                # Izohlar
                for full_name, matn in post_data['comments']:
                    Comment.objects.create(
                        murojaat=murojaat,
                        telegram_user_id=4000000 + random.randint(1, 99999),
                        telegram_full_name=full_name,
                        matn=matn,
                    )

                self.stdout.write(f"  ✓ Lenta: {post_data['izoh'][:50]}...")

            self.stdout.write(self.style.SUCCESS(f"3 ta lenta posti yaratildi!"))
