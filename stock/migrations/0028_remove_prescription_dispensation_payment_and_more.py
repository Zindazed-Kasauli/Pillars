# Generated by Django 4.0.6 on 2022-09-15 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0027_dosage_unit_cost_alter_prescription_stashed_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='dispensation_payment',
        ),
        migrations.AddField(
            model_name='dispensationpayment',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispensation_prescriptions', to='stock.prescription'),
        ),
    ]