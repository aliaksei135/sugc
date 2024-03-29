# Generated by Django 2.2.9 on 2020-04-30 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import sugc.validators


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
            name='FeesInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Flying Date')),
                ('balance', models.FloatField(default=0.0, verbose_name='Flying Fees Due')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
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
                ('junior_subs_mins', models.IntegerField(verbose_name="Juniors' Subsidised Amount of Minutes")),
                ('junior_subs_launch_cost', models.FloatField(verbose_name="Juniors' Subsidised Launch Cost")),
                ('junior_subs_tlf_cost', models.FloatField(verbose_name="Juniors' Subsidised TLF Cost")),
                ('junior_subs_minute_cost', models.FloatField(verbose_name="Juniors' Subsidised Minute Cost")),
                ('std_launch_cost', models.FloatField(verbose_name='Standard Actual Launch Cost')),
                ('std_tlf_cost', models.FloatField(verbose_name='Standard Actual TLF Cost')),
                ('std_minute_cost', models.FloatField(verbose_name='Standard Actual Minute Cost')),
                ('std_subs_mins', models.IntegerField(verbose_name='Standard Subsidised Amount of Minutes')),
                ('std_subs_launch_cost', models.FloatField(verbose_name='Standard Subsidised Launch Cost')),
                ('std_subs_tlf_cost', models.FloatField(verbose_name='Standard Subsidised TLF Cost')),
                ('std_subs_minute_cost', models.FloatField(verbose_name='Standard Subsidised Minute Cost')),
                ('std_age', models.IntegerField(default=26, verbose_name='Age from which to charge standard fees')),
            ],
            options={
                'ordering': ['-date_effective_from'],
            },
        ),
        migrations.CreateModel(
            name='FlyingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True, verbose_name='Flying List Date')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='flyinglists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
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
                ('invoiced_for', models.BooleanField(default=False, editable=False, verbose_name='Invoiced For')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sugc.Aircraft')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                              to='sugc.FeesInvoice')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flights',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Time Added')),
                ('date_available',
                 models.DateField(validators=[sugc.validators.not_in_past_validator], verbose_name='Available')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability',
                                             to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Available Day',
                'verbose_name_plural': 'Availability',
            },
        ),
    ]
