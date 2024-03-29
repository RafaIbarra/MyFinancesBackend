# Generated by Django 5.0.2 on 2024-02-21 03:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conexion', '0010_meses_numero_mes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='nombre_gasto',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productosfinancieros',
            name='nombre_producto',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='sesionesactivas',
            name='expiracion_conexion',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 3, 34, 34, 511717, tzinfo=datetime.timezone.utc)),
        ),
    ]
