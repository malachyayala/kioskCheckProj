# Generated by Django 3.2.25 on 2024-06-06 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0003_alter_kioskcheck_completed_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kioskcheck',
            name='charging_station',
        ),
    ]
