# Generated by Django 3.2 on 2021-05-25 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210520_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=70)),
                ('phone', models.IntegerField(default='')),
                ('review', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
    ]
