# Generated by Django 3.2.25 on 2024-06-04 19:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kioskcheck',
            name='completed_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 4, 19, 38, 36, 755965, tzinfo=utc)),
        ),
    ]
