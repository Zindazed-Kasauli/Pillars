# Generated by Django 4.0.6 on 2022-09-15 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0026_alter_dosage_frequency_alter_dosage_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosage',
            name='unit_cost',
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prescription',
            name='stashed_amount',
            field=models.FloatField(default=0),
        ),
    ]
