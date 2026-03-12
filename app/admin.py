from django.contrib import admin
from .models import Murojaat, Statistika


@admin.register(Murojaat)
class MurojaatAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_full_name', 'telegram_user_id', 'viloyat', 'tuman', 'infratuzilma', 'holat', 'yuborilgan_vaqt')
    list_filter = ('holat', 'viloyat', 'infratuzilma')
    search_fields = ('telegram_full_name', 'telegram_username', 'tuman', 'izoh')
    list_editable = ('holat',)
    readonly_fields = ('yuborilgan_vaqt', 'telegram_user_id')
    ordering = ('-yuborilgan_vaqt',)


@admin.register(Statistika)
class StatistikaAdmin(admin.ModelAdmin):
    list_display = ('id', 'maktablar_soni', 'bogchalar_soni', 'tibbiyot_soni', 'sport_soni', 'yangilangan_vaqt')
