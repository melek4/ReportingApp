# Generated by Django 4.0.3 on 2022-05-03 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('Direction', models.CharField(choices=[('Human_Ressources', 'Human_Ressources'), ('Finance', 'Finance')], default='Human_Ressources', max_length=50, verbose_name='Direction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ReportingApp.user',),
        ),
        migrations.CreateModel(
            name='Human_Ressources',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ReportingApp.user',),
        ),
    ]
