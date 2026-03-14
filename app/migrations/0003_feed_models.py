from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_murojaatfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='murojaat',
            name='is_anonim',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.BigIntegerField()),
                ('vaqt', models.DateTimeField(auto_now_add=True)),
                ('murojaat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.murojaat')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likelar',
                'unique_together': {('murojaat', 'telegram_user_id')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.BigIntegerField()),
                ('telegram_full_name', models.CharField(blank=True, max_length=200)),
                ('matn', models.TextField(max_length=500)),
                ('vaqt', models.DateTimeField(auto_now_add=True)),
                ('murojaat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.murojaat')),
            ],
            options={
                'verbose_name': 'Izoh',
                'verbose_name_plural': 'Izohlar',
                'ordering': ['-vaqt'],
            },
        ),
    ]
