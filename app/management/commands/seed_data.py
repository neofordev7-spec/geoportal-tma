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


# ─── Bog'chalar ─────────────────────────────────────────────────────────────
BOGCHALAR = [
    {
        'nom': "122-sonli bog'cha",
        'viloyat': 'toshkent_sh',
        'tuman': 'Sergeli tumani',
        'manzil': "Sergeli tumani, Qo'yliq ko'chasi 5",
        'rasm_url': '',
        'lat': 41.2245, 'lng': 69.2187,
        'vaadalar': [
            {'nom': "O'yin maydonini yangilash", 'tavsif': "Bolalar uchun xavfsiz o'yin jihozlari o'rnatish", 'icon': 'toys'},
            {'nom': "Oshxona jihozlarini almashtirish", 'tavsif': "Yangi elektr plita va muzlatgich", 'icon': 'restaurant'},
            {'nom': "Uxlash xonasini ta'mirlash", 'tavsif': "Yangi karavotlar va matraslar", 'icon': 'bed'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "O'yin maydoni yangilandi, bolalar xursand!", 30),
            ('bajarildi', "Oshxona jihozlari keldi", 31),
            ('muammo', "Karavotlar hali kelmadi", 32),
            ('bajarildi', "Hammasi yaxshi", 30),
        ]
    },
    {
        'nom': "56-sonli bog'cha",
        'viloyat': 'samarqand',
        'tuman': 'Samarqand shahri',
        'manzil': "Samarqand shahri, Mirzo Ulug'bek ko'chasi 18",
        'rasm_url': '',
        'lat': 39.6612, 'lng': 66.9407,
        'vaadalar': [
            {'nom': 'Isitish tizimini yangilash', 'tavsif': "Qish uchun gaz isitgichlarini o'rnatish", 'icon': 'local_fire_department'},
            {'nom': 'Gigiena vositalari', 'tavsif': "Sovun, sanitizer va sochiqlar ta'minoti", 'icon': 'soap'},
            {'nom': "Bolalar mebeli", 'tavsif': "Yangi stol va stulchalar", 'icon': 'chair'},
        ],
        'tekshiruvlar': [
            ('muammo', "Isitish hali ta'mirlanmadi", 33),
            ('muammo', "Sovun yo'q", 34),
            ('muammo', "Stulchalar singan", 33),
        ]
    },
    {
        'nom': "87-sonli bog'cha",
        'viloyat': 'toshkent_sh',
        'tuman': 'Olmazor tumani',
        'manzil': 'Olmazor tumani, Chorsu ko\'chasi 9',
        'rasm_url': '',
        'lat': 41.3312, 'lng': 69.2176,
        'vaadalar': [
            {'nom': "Hovlidagi daraxtlarni parvarish qilish", 'tavsif': "Ko'chatlar ekish va obodonlashtirish", 'icon': 'park'},
            {'nom': 'Xavfsizlik kameralari', 'tavsif': "Bog'cha hududida 6 ta kamera o'rnatish", 'icon': 'videocam'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Daraxtlar ekildi, juda chiroyli!", 35),
            ('bajarildi', "Kameralar o'rnatildi", 36),
            ('bajarildi', "Bolalar xavfsiz muhitda", 35),
        ]
    },
    {
        'nom': "34-sonli bog'cha",
        'viloyat': 'fargona',
        'tuman': "Farg'ona shahri",
        'manzil': "Farg'ona shahri, Al-Farg'oniy ko'chasi 7",
        'rasm_url': '',
        'lat': 40.3802, 'lng': 71.7803,
        'vaadalar': [
            {'nom': "Ichimlik suvi filtri", 'tavsif': "Bolalar uchun toza ichimlik suvi", 'icon': 'water_drop'},
            {'nom': "Yangi o'yinchoqlar", 'tavsif': "Rivojlantiruvchi o'yinchoqlar to'plami", 'icon': 'smart_toy'},
            {'nom': "Tom ta'mirlash", 'tavsif': "Oqayotgan tomni ta'mirlash", 'icon': 'roofing'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Suv filtri o'rnatildi", 37),
            ('muammo', "O'yinchoqlar kelmadi", 38),
            ('bajarildi', "Tom ta'mirlandi", 37),
        ]
    },
    {
        'nom': "15-sonli bog'cha",
        'viloyat': 'andijon',
        'tuman': 'Asaka tumani',
        'manzil': 'Asaka tumani, Navoiy ko\'chasi 3',
        'rasm_url': '',
        'lat': 40.6321, 'lng': 72.2243,
        'vaadalar': [
            {'nom': "Elektr simlarini yangilash", 'tavsif': "Xavfsiz elektr tarmog'i", 'icon': 'electric_bolt'},
            {'nom': "Asfalt yo'lka", 'tavsif': "Bog'cha ichidagi yo'lkalarni asfaltlash", 'icon': 'road'},
        ],
        'tekshiruvlar': []
    },
]

# ─── Shifoxonalar ────────────────────────────────────────────────────────────
SHIFOXONALAR = [
    {
        'nom': 'Yunusobod tuman oilaviy poliklinikasi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Yunusobod tumani',
        'manzil': "Yunusobod tumani, Bog'ishamol ko'chasi 21",
        'rasm_url': '',
        'lat': 41.3412, 'lng': 69.2976,
        'vaadalar': [
            {'nom': "Rentgen apparatini yangilash", 'tavsif': "Yangi raqamli rentgen apparati o'rnatish", 'icon': 'radiology'},
            {'nom': "Kutish zali ta'mirlash", 'tavsif': "Bemorlar uchun qulay sharoit yaratish", 'icon': 'weekend'},
            {'nom': "Laboratoriya jihozlari", 'tavsif': "Qon tahlili apparatlari va reagentlar", 'icon': 'biotech'},
            {'nom': "Tibbiy kiyimlar", 'tavsif': "Shifokorlar uchun yangi forma", 'icon': 'checkroom'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Rentgen yangilandi, juda sifatli!", 40),
            ('bajarildi', "Kutish zali chiroyli ta'mirlandi", 41),
            ('muammo', "Laboratoriya jihozlari to'liq emas", 42),
            ('bajarildi', "Yangi formalar berildi", 40),
        ]
    },
    {
        'nom': 'Qarshi shahar tibbiyot markazi',
        'viloyat': 'qashqadaryo',
        'tuman': 'Qarshi shahri',
        'manzil': "Qarshi shahri, Mustaqillik ko'chasi 45",
        'rasm_url': '',
        'lat': 38.8571, 'lng': 65.8011,
        'vaadalar': [
            {'nom': 'Tez yordam mashinasi', 'tavsif': "2 ta yangi tez yordam mashinasi sotib olish", 'icon': 'local_shipping'},
            {'nom': 'Reanimatsiya bo\'limi', 'tavsif': "Yangi reanimatsiya jihozlari", 'icon': 'monitor_heart'},
            {'nom': "Dorixona ta'minoti", 'tavsif': "Bepul dorilar ta'minoti", 'icon': 'medication'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "1 ta yangi mashina keldi", 43),
            ('muammo', "Reanimatsiya jihozlari hali kelmadi", 44),
            ('muammo', "Dorilar yetarli emas", 43),
            ('bajarildi', "Mashina zo'r ishlayapti", 45),
        ]
    },
    {
        'nom': 'Chilonzor tuman stomatologiyasi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Chilonzor tumani',
        'manzil': "Chilonzor tumani, Qatortol ko'chasi 12",
        'rasm_url': '',
        'lat': 41.2715, 'lng': 69.1876,
        'vaadalar': [
            {'nom': 'Yangi stomatologik kreslo', 'tavsif': "3 ta yangi stomatologik kreslo o'rnatish", 'icon': 'dentistry'},
            {'nom': 'Sterilizatsiya uskunalari', 'tavsif': "Yangi avtoklav va sterilizator", 'icon': 'local_laundry_service'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Kreslolar o'rnatildi, zo'r!", 46),
            ('bajarildi', "Sterilizator ishlayapti", 47),
            ('bajarildi', "Tozalik ajoyib", 46),
        ]
    },
    {
        'nom': "Namangan viloyat ko'z kasalliklari shifoxonasi",
        'viloyat': 'namangan',
        'tuman': 'Namangan shahri',
        'manzil': "Namangan shahri, Bobur ko'chasi 15",
        'rasm_url': '',
        'lat': 41.0023, 'lng': 71.6636,
        'vaadalar': [
            {'nom': "Ko'z operatsiyasi jihozlari", 'tavsif': "Lazer operatsiya uskunasi", 'icon': 'visibility'},
            {'nom': "Bemor palatalarini yangilash", 'tavsif': "Karavotlar va konditsionerlar", 'icon': 'bed'},
            {'nom': "Parkovka joyi", 'tavsif': "Bemorlar uchun avtoturargoh", 'icon': 'local_parking'},
        ],
        'tekshiruvlar': [
            ('muammo', "Lazer jihozi hali kelmadi", 48),
            ('bajarildi', "Palatalar yangilandi", 49),
            ('muammo', "Parkovka juda tor", 48),
        ]
    },
    {
        'nom': 'Buxoro tuman tibbiyot birlashmasi',
        'viloyat': 'buxoro',
        'tuman': 'Buxoro shahri',
        'manzil': "Buxoro shahri, Ibn Sino ko'chasi 8",
        'rasm_url': '',
        'lat': 39.7687, 'lng': 64.4216,
        'vaadalar': [
            {'nom': "Ultratovush apparati", 'tavsif': "Yangi UZI apparati sotib olish", 'icon': 'pregnant_woman'},
            {'nom': "Shifoxona hovlisi", 'tavsif': "Ko'kalamzorlashtirish va orom zonasi", 'icon': 'park'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "UZI apparati keldi, ishlamoqda!", 50),
            ('bajarildi', "Hovli juda chiroyli qilindi", 51),
        ]
    },
]

# ─── Sport inshootlari ──────────────────────────────────────────────────────
SPORT_INSHOOTLARI = [
    {
        'nom': 'Yunusobod sport kompleksi',
        'viloyat': 'toshkent_sh',
        'tuman': 'Yunusobod tumani',
        'manzil': "Yunusobod tumani, Sport ko'chasi 10",
        'rasm_url': '',
        'lat': 41.3452, 'lng': 69.2856,
        'vaadalar': [
            {'nom': "Suzish havzasini ta'mirlash", 'tavsif': "Suv filtrlash va isitish tizimini yangilash", 'icon': 'pool'},
            {'nom': 'Trenajor zalini jihozlash', 'tavsif': "20 ta yangi trenajor o'rnatish", 'icon': 'fitness_center'},
            {'nom': "Yoritish tizimi", 'tavsif': "LED chiroqlar bilan almashtirish", 'icon': 'lightbulb'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Havza ta'mirlandi, suv toza!", 55),
            ('bajarildi', "Trenajorlar o'rnatildi", 56),
            ('bajarildi', "Chiroqlar yangilandi", 55),
        ]
    },
    {
        'nom': 'Samarqand shahri futbol stadioni',
        'viloyat': 'samarqand',
        'tuman': 'Samarqand shahri',
        'manzil': "Samarqand shahri, Registon ko'chasi 20",
        'rasm_url': '',
        'lat': 39.6582, 'lng': 66.9657,
        'vaadalar': [
            {'nom': "Sun'iy o't qoplama", 'tavsif': "FIFA standartidagi sun'iy o't yotqizish", 'icon': 'grass'},
            {'nom': 'Tomoshabinlar joylari', 'tavsif': "2000 ta yangi o'rindiq o'rnatish", 'icon': 'chair'},
            {'nom': "Yoritish minorasi", 'tavsif': "4 ta 30m yoritish minorasini o'rnatish", 'icon': 'fluorescent'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "O't yotqizildi, zo'r sifat!", 57),
            ('muammo', "O'rindiqlar hali o'rnatilmadi", 58),
            ('muammo', "Yoritish minoralari kelmadi", 57),
        ]
    },
    {
        'nom': "Farg'ona viloyat tennis korti",
        'viloyat': 'fargona',
        'tuman': "Farg'ona shahri",
        'manzil': "Farg'ona shahri, Navoiy ko'chasi 30",
        'rasm_url': '',
        'lat': 40.3862, 'lng': 71.7903,
        'vaadalar': [
            {'nom': "Kort qoplamasi", 'tavsif': "Tennis kort qoplamasini yangilash", 'icon': 'sports_tennis'},
            {'nom': 'Kiyinish xonalari', 'tavsif': "Dush va kiyinish xonalarini ta'mirlash", 'icon': 'shower'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Qoplama yangilandi", 59),
            ('muammo', "Dush xonasi ishlamayapti", 60),
        ]
    },
    {
        'nom': "Andijon bolalar sport maktabi",
        'viloyat': 'andijon',
        'tuman': 'Andijon shahri',
        'manzil': "Andijon shahri, Mustaqillik ko'chasi 15",
        'rasm_url': '',
        'lat': 40.7861, 'lng': 72.3502,
        'vaadalar': [
            {'nom': 'Gimnastika zali', 'tavsif': "Gimnastika jihozlarini yangilash", 'icon': 'sports_gymnastics'},
            {'nom': 'Boks ringi', 'tavsif': "Yangi boks ringi va qo'lqoplar", 'icon': 'sports_mma'},
            {'nom': "Bolalar uchun sport inventar", 'tavsif': "To'plar, skakalka va boshqa inventar", 'icon': 'sports_handball'},
        ],
        'tekshiruvlar': [
            ('bajarildi', "Gimnastika jihozlari zo'r!", 61),
            ('bajarildi', "Boks ringi o'rnatildi", 62),
            ('muammo', "Inventar yetarli emas", 61),
        ]
    },
    {
        'nom': "Xorazm suzish baseyni",
        'viloyat': 'xorazm',
        'tuman': 'Urganch shahri',
        'manzil': "Urganch shahri, Al-Xorazmiy ko'chasi 5",
        'rasm_url': '',
        'lat': 41.5531, 'lng': 60.6245,
        'vaadalar': [
            {'nom': "Basseyn filtrlash tizimi", 'tavsif': "Yangi filtrlash va xlor tizimi", 'icon': 'water'},
            {'nom': "Tomoshabin joylari", 'tavsif': "Oila a'zolari uchun o'tirish joylari", 'icon': 'weekend'},
        ],
        'tekshiruvlar': []
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

        # Barcha obyekt turlarini birlashtirish
        BARCHA_OBYEKTLAR = [
            ('maktab', MAKTABLAR),
            ('bogcha', BOGCHALAR),
            ('shifoxona', SHIFOXONALAR),
            ('sport', SPORT_INSHOOTLARI),
        ]

        created = 0
        for tur, obyektlar in BARCHA_OBYEKTLAR:
            for data in obyektlar:
                maktab, new = Maktab.objects.get_or_create(
                    nom=data['nom'],
                    defaults={
                        'tur': tur,
                        'viloyat': data['viloyat'],
                        'tuman': data['tuman'],
                        'manzil': data['manzil'],
                        'rasm_url': data.get('rasm_url', ''),
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

                # Obyekt holatini yangilash
                jami = Tekshiruv.objects.filter(maktab=maktab).count()
                if jami > 0:
                    baj = Tekshiruv.objects.filter(maktab=maktab, natija='bajarildi').count()
                    foiz = round(baj / jami * 100)
                    maktab.holat = 'yaxshi' if foiz >= 70 else 'etiborga_muhtoj' if foiz >= 40 else 'nosoz'
                    maktab.save(update_fields=['holat'])

                created += 1
                self.stdout.write(f"  ✓ [{tur}] {maktab.nom}")

        if created:
            self.stdout.write(self.style.SUCCESS(f"\n{created} ta obyekt muvaffaqiyatli yaratildi!"))
        else:
            self.stdout.write(self.style.WARNING("Ma'lumotlar allaqachon mavjud."))

        jami_t = Tekshiruv.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Jami tekshiruvlar: {jami_t} ta"))

        # ── Lenta postlari ──────────────────────────────────────
        self.stdout.write("\nLenta postlari yuklanmoqda...")
        # Tartib: birinchi rasmli (feedda oxirida), keyin videolar (feedda tepada)
        LENTA_POSTS = [
            {
                'izoh': "Va'dalar beriladi, muammo esa echilmaydi: Guliston mahallasining chang va loy ko'chasi qachondir ta'mirlanadimi?\n\nQashqadaryo viloyati Qarshi tumanidagi Guliston mahallasi aholisi tuman hokimligi tomonidan yillar davomida berilayotgan va'dalar bajarilmayotgani yuzasidan murojaat yo'lladi.",
                'viloyat': 'qashqadaryo',
                'tuman': 'Qarshi tumani',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000003,
                'telegram_full_name': 'Anonim fuqaro',
                'is_anonim': True,
                'holat': 'kutilmoqda',
                'media': ['/media/lenta/kocha.jpg', '/media/lenta/kocha3.jpg', '/media/lenta/kochaq.jpg'],
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
            {
                'izoh': "Asfalt yo'limiz qurib berildi, juda xursandmiz! Rahmat hukumatga!",
                'viloyat': 'qashqadaryo',
                'tuman': 'Qarshi shahri',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000002,
                'telegram_full_name': 'Malika Yusupova',
                'is_anonim': False,
                'holat': 'hal_qilindi',
                'media': ['/media/lenta/asfalt.mp4'],
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
                'izoh': "Qarshi–Shahrisabz magistral yo'li ta'miri nega to'xtab qoldi?\n\nQarshi–Shahrisabz magistral avtomobil yo'lining Yakkabog' tumanidan o'tgan qismida olib borilayotgan ta'mirlash ishlari o'tgan yil dekabr oyidan beri to'xtab qolgan.",
                'viloyat': 'qashqadaryo',
                'tuman': 'Yakkabog\'',
                'infratuzilma': 'yol',
                'telegram_user_id': 2000001,
                'telegram_full_name': 'Dilshod Rahmatov',
                'is_anonim': False,
                'holat': 'kutilmoqda',
                'media': ['/media/lenta/qarshi_yakkaboq.mp4'],
                'likes': 47,
                'comments': [
                    ('Jasur Toshev', "Bu yo'ldan har kuni o'taman, juda xavfli holatda!"),
                    ('Nilufar K.', "O'tgan yili ham shunday edi, va'da berishdi lekin hech narsa qilishmadi"),
                    ('Sardor M.', "Hokimlikka murojaatlar yubordik, javob yo'q"),
                    ('Zulfiya A.', "Yomg'ir yog'sa loy bo'lib ketadi, mashinalar buziladi"),
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
