# Generated by Django 5.0.1 on 2024-01-14 21:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Il',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=250)),
                ('long_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('long_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='created_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='deleted_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'İl',
                'verbose_name_plural': 'İller',
                'db_table': 'il',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ilce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=250)),
                ('long_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('long_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='created_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='deleted_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('il', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.il')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'İlçe',
                'verbose_name_plural': 'İlçeler',
                'db_table': 'ilce',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MahalleKoy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=250)),
                ('semt_bucak_belde', models.CharField(blank=True, max_length=255, null=True)),
                ('posta_kodu', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('mahalle', 'mahalle'), ('koy', 'koy')], default='mahalle', max_length=20)),
                ('long_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('long_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='created_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='deleted_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('il', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.il')),
                ('ilce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.ilce')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mahalle/Köy',
                'verbose_name_plural': 'Mahalle/Köyler',
                'db_table': 'mahallekoy',
                'ordering': ['ilce', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Sokak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=250)),
                ('long_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_min', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('long_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat_max', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='created_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='deleted_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('il', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.il')),
                ('ilce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.ilce')),
                ('mahallekoy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.mahallekoy')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='updated_by_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sokak',
                'verbose_name_plural': 'Sokaklar',
                'db_table': 'sokak',
                'ordering': ['il', 'ilce', 'mahallekoy', 'name'],
            },
        ),
    ]