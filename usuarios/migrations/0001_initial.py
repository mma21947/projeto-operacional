# Generated by Django 5.1.7 on 2025-03-20 19:39

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
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('admin', 'Administrador'), ('comum', 'Usuário Comum')], default='comum', max_length=20, verbose_name='Tipo de Perfil')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='perfil/', verbose_name='Foto de Perfil')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('ultimo_acesso', models.DateTimeField(blank=True, null=True, verbose_name='Último Acesso')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfis',
                'ordering': ['usuario__username'],
            },
        ),
    ]
