# Generated by Django 3.2.7 on 2021-10-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211008_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
