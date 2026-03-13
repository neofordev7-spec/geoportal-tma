from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Statistika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('maktablar_soni', models.IntegerField(default=11139)),
                ('bogchalar_soni', models.IntegerField(default=6935)),
                ('tibbiyot_soni', models.IntegerField(default=3034)),
                ('sport_soni', models.IntegerField(default=356)),
                ('yangilangan_vaqt', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Statistika', 'verbose_name_plural': 'Statistika'},
        ),
        migrations.CreateModel(
            name='Maktab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=200)),
                ('viloyat', models.CharField(max_length=100, choices=[('toshkent_sh','Toshkent shahri'),('toshkent_v','Toshkent viloyati'),('samarqand','Samarqand viloyati'),('fargona',"Farg'ona viloyati"),('andijon','Andijon viloyati'),('namangan','Namangan viloyati'),('buxoro','Buxoro viloyati'),('xorazm','Xorazm viloyati'),('qashqadaryo',"Qashqadaryo viloyati"),('surxondaryo','Surxondaryo viloyati'),('jizzax','Jizzax viloyati'),('sirdaryo','Sirdaryo viloyati'),('navoiy',"Navoiy viloyati"),('qoraqalpogiston',"Qoraqalpog'iston Respublikasi")])),
                ('tuman', models.CharField(max_length=100)),
                ('manzil', models.TextField()),
                ('rasm_url', models.URLField(blank=True)),
                ('lat', models.FloatField(default=41.2995)),
                ('lng', models.FloatField(default=69.2401)),
                ('holat', models.CharField(choices=[('yaxshi','Yaxshi'),('etiborga_muhtoj',"E'tiborga muhtoj"),('nosoz','Nosoz')], default='yaxshi', max_length=30)),
                ('qoshilgan_vaqt', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['nom'], 'verbose_name': 'Maktab', 'verbose_name_plural': 'Maktablar'},
        ),
        migrations.CreateModel(
            name='Murojaat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('rasm', models.ImageField(blank=True, null=True, upload_to='murojaatlar/')),
                ('viloyat', models.CharField(max_length=100, choices=[('toshkent_sh','Toshkent shahri'),('toshkent_v','Toshkent viloyati'),('samarqand','Samarqand viloyati'),('fargona',"Farg'ona viloyati"),('andijon','Andijon viloyati'),('namangan','Namangan viloyati'),('buxoro','Buxoro viloyati'),('xorazm','Xorazm viloyati'),('qashqadaryo',"Qashqadaryo viloyati"),('surxondaryo','Surxondaryo viloyati'),('jizzax','Jizzax viloyati'),('sirdaryo','Sirdaryo viloyati'),('navoiy',"Navoiy viloyati"),('qoraqalpogiston',"Qoraqalpog'iston Respublikasi")])),
                ('tuman', models.CharField(max_length=100)),
                ('infratuzilma', models.CharField(max_length=50, choices=[('maktab','Maktab'),('bogcha',"Bog'cha"),('shifoxona','Shifoxona'),('yol',"Yo'l infratuzilmasi"),('sport','Sport inshootlari'),('boshqa','Boshqa')])),
                ('sektor', models.CharField(max_length=50)),
                ('izoh', models.TextField(blank=True)),
                ('telegram_user_id', models.BigIntegerField()),
                ('telegram_username', models.CharField(blank=True, max_length=150)),
                ('telegram_full_name', models.CharField(blank=True, max_length=200)),
                ('yuborilgan_vaqt', models.DateTimeField(auto_now_add=True)),
                ('holat', models.CharField(choices=[('kutilmoqda','Kutilmoqda'),('korib_chiqilmoqda',"Ko'rib chiqilmoqda"),('hal_qilindi','Hal qilindi')], default='kutilmoqda', max_length=50)),
            ],
            options={'ordering': ['-yuborilgan_vaqt'], 'verbose_name': 'Murojaat', 'verbose_name_plural': 'Murojaatlar'},
        ),
        migrations.CreateModel(
            name='MurojaatRasm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('rasm', models.ImageField(upload_to='murojaatlar/')),
                ('murojaat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rasmlar', to='app.murojaat')),
            ],
            options={'verbose_name': 'Murojaat rasmi', 'verbose_name_plural': 'Murojaat rasmlari'},
        ),
        migrations.CreateModel(
            name='Vaada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=300)),
                ('tavsif', models.TextField(blank=True)),
                ('icon', models.CharField(default='build', max_length=50)),
                ('tartib', models.IntegerField(default=0)),
                ('maktab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaadalar', to='app.maktab')),
            ],
            options={'ordering': ['tartib', 'id'], 'verbose_name': "Va'da", 'verbose_name_plural': "Va'dalar"},
        ),
        migrations.CreateModel(
            name='Tekshiruv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('natija', models.CharField(choices=[('bajarildi','Bajarildi ✓'),('muammo','Muammo ✗')], max_length=20)),
                ('rasm', models.ImageField(blank=True, null=True, upload_to='tekshiruvlar/')),
                ('izoh', models.TextField(blank=True)),
                ('telegram_user_id', models.BigIntegerField()),
                ('telegram_username', models.CharField(blank=True, max_length=150)),
                ('telegram_full_name', models.CharField(blank=True, max_length=200)),
                ('vaqt', models.DateTimeField(auto_now_add=True)),
                ('maktab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tekshiruvlar', to='app.maktab')),
                ('vaada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tekshiruvlar', to='app.vaada')),
            ],
            options={'ordering': ['-vaqt'], 'verbose_name': 'Tekshiruv', 'verbose_name_plural': 'Tekshiruvlar'},
        ),
    ]
