# Generated by Django 2.2.9 on 2020-02-28 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sugc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flyinglist',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flyinglist',
            name='members',
            field=models.ManyToManyField(related_name='flyinglists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flight',
            name='aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sugc.Aircraft'),
        ),
        migrations.AddField(
            model_name='flight',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feesinvoice',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='availability',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
