# Generated by Django 3.0.3 on 2020-05-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200501_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
