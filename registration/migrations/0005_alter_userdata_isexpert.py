# Generated by Django 4.1.7 on 2023-04-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_userdata_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='isexpert',
            field=models.BooleanField(default=True),
        ),
    ]
