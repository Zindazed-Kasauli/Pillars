# Generated by Django 4.0.6 on 2022-09-11 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_remove_dosage_stock_item_dosage_stock_batch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispensationpayment',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]