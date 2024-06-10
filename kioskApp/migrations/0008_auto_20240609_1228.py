# Generated by Django 3.2.25 on 2024-06-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kioskApp', '0007_kioskcheck_computer_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingstationcheck',
            name='charger_status',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chargingstationcheck',
            name='issue_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chargingstationcheck',
            name='location',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kioskcheck',
            name='computer_issue',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]