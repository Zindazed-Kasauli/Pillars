# Generated by Django 4.0.6 on 2022-09-19 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0031_rename_dosage_stockbatch_dosages'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockbatch',
            name='total_quantity',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
