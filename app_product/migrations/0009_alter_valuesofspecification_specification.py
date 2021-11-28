# Generated by Django 3.2.8 on 2021-11-27 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0008_alter_valuesofspecification_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuesofspecification',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values_sp', to='app_product.specification', verbose_name='Характеристика'),
        ),
    ]
