# Generated by Django 3.2.25 on 2024-06-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0011_delete_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrinterLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]