# Generated by Django 5.0.6 on 2024-05-25 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnero', '0002_turno_fecha_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='dni',
            field=models.CharField(default='00000000', max_length=100, unique=True),
        ),
    ]