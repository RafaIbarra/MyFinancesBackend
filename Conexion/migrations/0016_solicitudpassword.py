# Generated by Django 5.0.2 on 2024-03-15 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conexion', '0015_alter_categoriagastos_nombre_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudPassword',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_recuperacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(verbose_name='fecha creacion')),
                ('fecha_vencimiento', models.DateTimeField(verbose_name='fecha vencimiento')),
                ('fecha_procesamiento', models.DateTimeField(blank=True, verbose_name='fecha vencimiento')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Conexion.usuarios')),
            ],
            options={
                'db_table': 'SolicitudPassword',
            },
        ),
    ]