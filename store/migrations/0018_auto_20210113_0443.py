# Generated by Django 3.1.2 on 2021-01-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210113_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(default='logo.png', upload_to=''),
        ),
    ]
