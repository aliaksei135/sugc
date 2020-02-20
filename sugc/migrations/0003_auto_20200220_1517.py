# Generated by Django 2.2.9 on 2020-02-20 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sugc', '0002_flight_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='member',
        ),
        migrations.AddField(
            model_name='flight',
            name='member',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
