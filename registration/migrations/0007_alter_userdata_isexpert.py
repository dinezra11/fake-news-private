# Generated by Django 4.1.7 on 2023-04-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_userdata_certificate_userdata_isadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='isexpert',
            field=models.BooleanField(default=False),
        ),
    ]
