# Generated by Django 3.0.3 on 2020-05-29 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20200529_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='category',
            field=models.CharField(choices=[('1', 'New'), ('2', 'Impulsive'), ('3', 'Discount'), ('4', 'Loyal')], default='New', max_length=50, null=True),
        ),
    ]
