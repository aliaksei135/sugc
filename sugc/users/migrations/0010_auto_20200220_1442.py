# Generated by Django 2.2.9 on 2020-02-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0009_auto_20200220_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='flights',
            field=models.ManyToManyField(to='sugc.Flight'),
        ),
    ]