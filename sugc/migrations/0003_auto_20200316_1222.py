# Generated by Django 2.2.9 on 2020-03-16 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sugc', '0002_auto_20200304_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flyinglist',
            name='date',
            field=models.DateField(unique=True, verbose_name='Flying List Date'),
        ),
    ]
