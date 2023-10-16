# Generated by Django 4.2.5 on 2023-10-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghapp', '0006_remove_culturetype_reqhum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='culturetype',
            name='ReqHum',
            field=models.DecimalField(decimal_places=2, default=25, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='culturetype',
            name='ReqTempC',
            field=models.DecimalField(decimal_places=2, default=23, max_digits=5),
            preserve_default=False,
        ),
    ]
