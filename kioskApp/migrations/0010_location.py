# Generated by Django 3.2.25 on 2024-06-10 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0009_alter_chargingstationcheck_charger_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
