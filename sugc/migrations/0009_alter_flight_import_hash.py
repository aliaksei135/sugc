# Generated by Django 3.2.6 on 2023-03-16 00:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sugc', '0008_flight_import_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='import_hash',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Import Hash'),
        ),
    ]