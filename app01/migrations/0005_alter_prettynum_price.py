# Generated by Django 3.2.20 on 2023-09-20 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_prettynum_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prettynum',
            name='price',
            field=models.IntegerField(default=0, verbose_name='价格'),
        ),
    ]
