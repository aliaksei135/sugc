# Generated by Django 2.2.9 on 2020-07-10 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sugc', '0004_glidingfeegroup_daily_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glidingfeegroup',
            name='applicability_condition',
            field=models.CharField(default='False', max_length=300, verbose_name='Applicability Condition'),
        ),
    ]
