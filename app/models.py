from django.db import models
from django.db.models import Count, Q


INFRATUZILMA_TURLARI = [
    ('maktab', 'Maktab'),
    ('bogcha', "Bog'cha"),
    ('shifoxona', 'Shifoxona'),
    ('yol', "Yo'l infratuzilmasi"),
    ('sport', 'Sport inshootlari'),
    ('boshqa', 'Boshqa'),
]

HOLAT_TURLARI = [
    ('kutilmoqda', 'Kutilmoqda'),
    ('korib_chiqilmoqda', "Ko'rib chiqilmoqda"),
    ('hal_qilindi', 'Hal qilindi'),
]

VILOYATLAR = [
    ('toshkent_sh', 'Toshkent shahri'),
    ('toshkent_v', 'Toshkent viloyati'),
    ('samarqand', 'Samarqand viloyati'),
    ('fargona', "Farg'ona viloyati"),
    ('andijon', 'Andijon viloyati'),
    ('namangan', 'Namangan viloyati'),
    ('buxoro', 'Buxoro viloyati'),
    ('xorazm', 'Xorazm viloyati'),
    ('qashqadaryo', "Qashqadaryo viloyati"),
    ('surxondaryo', 'Surxondaryo viloyati'),
    ('jizzax', 'Jizzax viloyati'),
    ('sirdaryo', 'Sirdaryo viloyati'),
    ('navoiy', "Navoiy viloyati"),
    ('qoraqalpogiston', "Qoraqalpog'iston Respublikasi"),
]

MAKTAB_HOLAT = [
    ('yaxshi', 'Yaxshi'),
    ('etiborga_muhtoj', "E'tiborga muhtoj"),
    ('nosoz', 'Nosoz'),
]


class Murojaat(models.Model):
    rasm = models.ImageField(upload_to='murojaatlar/', blank=True, null=True)
    viloyat = models.CharField(max_length=100, choices=VILOYATLAR)
    tuman = models.CharField(max_length=100)
    infratuzilma = models.CharField(max_length=50, choices=INFRATUZILMA_TURLARI)
    sektor = models.CharField(max_length=50)
    izoh = models.TextField(blank=True)
    telegram_user_id = models.BigIntegerField()
    telegram_username = models.CharField(max_length=150, blank=True)
    telegram_full_name = models.CharField(max_length=200, blank=True)
    yuborilgan_vaqt = models.DateTimeField(auto_now_add=True)
    holat = models.CharField(max_length=50, choices=HOLAT_TURLARI, default='kutilmoqda')
    is_anonim = models.BooleanField(default=False)

    class Meta:
        ordering = ['-yuborilgan_vaqt']
        verbose_name = 'Murojaat'
        verbose_name_plural = 'Murojaatlar'

    def __str__(self):
        return f"{self.telegram_full_name or self.telegram_user_id} — {self.get_infratuzilma_display()} ({self.get_viloyat_display()})"


class MurojaatRasm(models.Model):
    murojaat = models.ForeignKey(Murojaat, on_delete=models.CASCADE, related_name='rasmlar')
    rasm = models.FileField(upload_to='murojaatlar/')

    class Meta:
        verbose_name = 'Murojaat rasmi'
        verbose_name_plural = 'Murojaat rasmlari'


class Statistika(models.Model):
    maktablar_soni = models.IntegerField(default=11139)
    bogchalar_soni = models.IntegerField(default=6935)
    tibbiyot_soni = models.IntegerField(default=3034)
    sport_soni = models.IntegerField(default=356)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistika'

    def __str__(self):
        return f"Statistika (yangilangan: {self.yangilangan_vaqt})"


# ─── Maktablar modeli ─────────────────────────────────────────────────────────

class Maktab(models.Model):
    nom = models.CharField(max_length=200)
    viloyat = models.CharField(max_length=100, choices=VILOYATLAR)
    tuman = models.CharField(max_length=100)
    manzil = models.TextField()
    rasm_url = models.URLField(blank=True)
    lat = models.FloatField(default=41.2995)
    lng = models.FloatField(default=69.2401)
    holat = models.CharField(max_length=30, choices=MAKTAB_HOLAT, default='yaxshi')
    qoshilgan_vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Maktab'
        verbose_name_plural = 'Maktablar'

    def __str__(self):
        return self.nom

    def mamnuniyat_foizi(self):
        """Bajarildi tekshiruvlar foizi"""
        jami = Tekshiruv.objects.filter(maktab=self).count()
        if jami == 0:
            return 0
        bajarildi = Tekshiruv.objects.filter(maktab=self, natija='bajarildi').count()
        return round(bajarildi / jami * 100)

    def tekshiruvlar_soni(self):
        return Tekshiruv.objects.filter(maktab=self).count()

    def holat_rangi(self):
        foiz = self.mamnuniyat_foizi()
        if foiz >= 70:
            return 'yaxshi'
        elif foiz >= 40:
            return 'etiborga_muhtoj'
        return 'nosoz'


class Vaada(models.Model):
    """Davlat har bir maktabga bergan va'dasi"""
    maktab = models.ForeignKey(Maktab, on_delete=models.CASCADE, related_name='vaadalar')
    nom = models.CharField(max_length=300)
    tavsif = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='build')
    tartib = models.IntegerField(default=0)

    class Meta:
        ordering = ['tartib', 'id']
        verbose_name = "Va'da"
        verbose_name_plural = "Va'dalar"

    def __str__(self):
        return f"{self.maktab.nom} — {self.nom}"

    def bajarildi_soni(self):
        return Tekshiruv.objects.filter(vaada=self, natija='bajarildi').count()

    def muammo_soni(self):
        return Tekshiruv.objects.filter(vaada=self, natija='muammo').count()

    def jami_tekshiruv(self):
        return Tekshiruv.objects.filter(vaada=self).count()

    def foiz(self):
        jami = self.jami_tekshiruv()
        if jami == 0:
            return None
        return round(self.bajarildi_soni() / jami * 100)


class Tekshiruv(models.Model):
    """Fuqaro tekshiruvi: bajarildi yoki muammo"""
    NATIJA = [
        ('bajarildi', 'Bajarildi ✓'),
        ('muammo', 'Muammo ✗'),
    ]
    maktab = models.ForeignKey(Maktab, on_delete=models.CASCADE, related_name='tekshiruvlar')
    vaada = models.ForeignKey(Vaada, on_delete=models.CASCADE, related_name='tekshiruvlar', null=True, blank=True)
    natija = models.CharField(max_length=20, choices=NATIJA)
    rasm = models.ImageField(upload_to='tekshiruvlar/', blank=True, null=True)
    izoh = models.TextField(blank=True)
    telegram_user_id = models.BigIntegerField()
    telegram_username = models.CharField(max_length=150, blank=True)
    telegram_full_name = models.CharField(max_length=200, blank=True)
    vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-vaqt']
        verbose_name = 'Tekshiruv'
        verbose_name_plural = 'Tekshiruvlar'

    def __str__(self):
        return f"{self.maktab.nom} — {self.get_natija_display()} — {self.telegram_full_name or self.telegram_user_id}"


# ─── Feed modellari ──────────────────────────────────────────────────────────

class Like(models.Model):
    murojaat = models.ForeignKey(Murojaat, on_delete=models.CASCADE, related_name='likes')
    telegram_user_id = models.BigIntegerField()
    vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('murojaat', 'telegram_user_id')
        verbose_name = 'Like'
        verbose_name_plural = 'Likelar'

    def __str__(self):
        return f"Like: {self.telegram_user_id} → Murojaat #{self.murojaat_id}"


class Comment(models.Model):
    murojaat = models.ForeignKey(Murojaat, on_delete=models.CASCADE, related_name='comments')
    telegram_user_id = models.BigIntegerField()
    telegram_full_name = models.CharField(max_length=200, blank=True)
    matn = models.TextField(max_length=500)
    vaqt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-vaqt']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.telegram_full_name}: {self.matn[:50]}"
