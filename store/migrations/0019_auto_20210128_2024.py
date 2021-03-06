# Generated by Django 3.1.2 on 2021-01-28 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210113_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='isVisible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
