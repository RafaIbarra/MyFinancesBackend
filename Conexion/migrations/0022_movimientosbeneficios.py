# Generated by Django 5.0.2 on 2024-06-02 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conexion', '0021_entidadesbeneficios'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientosBeneficios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.IntegerField()),
                ('fecha_beneficio', models.DateField(verbose_name='fecha beneficio')),
                ('anotacion', models.CharField(blank=True, max_length=200)),
                ('fecha_registro', models.DateTimeField(verbose_name='fecha registro')),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Conexion.entidadesbeneficios')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Conexion.usuarios')),
            ],
            options={
                'db_table': 'MovimientosBeneficios',
            },
        ),
    ]
