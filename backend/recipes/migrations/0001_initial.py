# Generated by Django 5.2.1 on 2025-06-03 10:01

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='name')),
                ('time', models.CharField(max_length=100, verbose_name='Tiempo')),
                ('photo', models.CharField(max_length=100, verbose_name='Foto')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='categories.category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
                'db_table': 'recipes',
            },
        ),
    ]
