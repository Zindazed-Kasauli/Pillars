# Generated by Django 4.0.6 on 2022-09-15 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0021_dosage_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosage',
            name='stock_batch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dosages', to='stock.stockbatch'),
        ),
    ]