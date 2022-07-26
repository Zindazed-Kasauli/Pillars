# Generated by Django 4.0.6 on 2022-09-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0028_remove_prescription_dispensation_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispensationpayment',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dosage',
            name='unit_cost',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='balance',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='bill',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='stashed_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stockbatch',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
