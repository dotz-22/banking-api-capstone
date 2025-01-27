# Generated by Django 5.1.5 on 2025-01-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_remove_transactionsmodel_transaction_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='transaction_type',
            field=models.CharField(choices=[('transfer', 'Transfer'), ('withdrawal', 'Withdrawal'), ('deposit', 'Deposit')], max_length=40),
        ),
    ]
