# Generated by Django 4.1.7 on 2023-05-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_predictionapproves_expertname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionapproves',
            name='title',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]