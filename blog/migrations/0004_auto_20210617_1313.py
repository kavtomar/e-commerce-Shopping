# Generated by Django 3.2 on 2021-06-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210617_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='chead3',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='head3',
            field=models.CharField(default='', max_length=500),
        ),
    ]