# Generated by Django 2.2.9 on 2020-07-10 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_user_is_alumni'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_third_party',
            field=models.BooleanField(default=False, verbose_name='Third Party?'),
        ),
    ]