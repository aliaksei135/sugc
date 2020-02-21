# Generated by Django 2.2.9 on 2020-02-21 23:30

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
            name='Aircraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration', models.CharField(max_length=5, unique=True, verbose_name='Registration')),
                ('type', models.CharField(max_length=255, verbose_name='Aircraft Type')),
                ('is_club_aircraft', models.BooleanField(verbose_name='Our Aircraft?')),
            ],
            options={
                'ordering': ['registration'],
            },
        ),
        migrations.CreateModel(
            name='GlidingFeePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_effective_from', models.DateField(verbose_name='Date Fees effective from')),
                ('junior_launch_cost', models.FloatField(verbose_name="Juniors' Actual Launch Cost")),
                ('junior_tlf_cost', models.FloatField(verbose_name="Juniors' Actual TLF Cost")),
                ('junior_minute_cost', models.FloatField(verbose_name="Juniors' Actual Minute Cost")),
                ('junior_subs_launch_cost', models.FloatField(verbose_name="Juniors' Subsidised Launch Cost")),
                ('junior_subs_tlf_cost', models.FloatField(verbose_name="Juniors' Subsidised TLF Cost")),
                ('junior_subs_minute_cost', models.FloatField(verbose_name="Juniors' Subsidised Minute Cost")),
                ('std_launch_cost', models.FloatField(verbose_name='Standard Actual Launch Cost')),
                ('std_tlf_cost', models.FloatField(verbose_name='Standard Actual TLF Cost')),
                ('std_minute_cost', models.FloatField(verbose_name='Standard Actual Minute Cost')),
                ('std_subs_launch_cost', models.FloatField(verbose_name='Standard Subsidised Launch Cost')),
                ('std_subs_tlf_cost', models.FloatField(verbose_name='Standard Subsidised TLF Cost')),
                ('std_subs_minute_cost', models.FloatField(verbose_name='Standard Subsidised Minute Cost')),
                ('std_age', models.IntegerField(verbose_name='Age at which to charge standard fees')),
            ],
            options={
                'ordering': ['-date_effective_from'],
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Flight Date')),
                ('capacity',
                 models.CharField(choices=[('P1', 'P1'), ('P2', 'P2'), ('EX', 'Examiner'), ('INS', 'Instructor')],
                                  default='P2', max_length=32, verbose_name='Pilot Capacity')),
                ('duration', models.DurationField(verbose_name='Flight Duration')),
                ('is_train_launch_failure', models.BooleanField(default=False, verbose_name='TLF?')),
                ('is_real_launch_failure', models.BooleanField(default=False, verbose_name='RLF?')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sugc.Aircraft')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
