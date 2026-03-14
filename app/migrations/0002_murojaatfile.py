from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='murojaatrasm',
            name='rasm',
            field=models.FileField(upload_to='murojaatlar/'),
        ),
    ]
