# Generated by Django 2.1.3 on 2018-12-06 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20181206_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='items/placeholder.png', upload_to='items'),
        ),
    ]
