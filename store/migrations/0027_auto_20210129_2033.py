# Generated by Django 3.1.2 on 2021-01-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_auto_20210129_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image6',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image7',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image8',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image1',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image2',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image3',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image4',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image5',
            field=models.ImageField(default='restaurant_defaultphoto.jpg', upload_to=''),
        ),
    ]
