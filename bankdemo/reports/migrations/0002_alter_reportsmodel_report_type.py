# Generated by Django 5.1.5 on 2025-02-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsmodel',
            name='report_type',
            field=models.CharField(choices=[('transaction_summary', 'Transaction_summary'), ('account_summary', 'Account_summary')], max_length=30),
        ),
    ]
