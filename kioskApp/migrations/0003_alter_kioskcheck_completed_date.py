# Generated by Django 3.2.25 on 2024-06-04 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0002_alter_kioskcheck_completed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kioskcheck',
            name='completed_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]