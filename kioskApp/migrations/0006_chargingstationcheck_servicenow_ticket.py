# Generated by Django 3.2.25 on 2024-06-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0005_chargingstationcheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingstationcheck',
            name='servicenow_ticket',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]