# Generated by Django 2.2.16 on 2022-02-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20220204_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre'),
        ),
    ]
