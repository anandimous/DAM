# Generated by Django 2.1.3 on 2018-12-06 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0005_client_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemloan',
            name='due_on',
            field=models.DateTimeField(null=True),
        ),
    ]