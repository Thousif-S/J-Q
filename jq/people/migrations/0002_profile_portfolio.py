# Generated by Django 2.2.3 on 2019-07-20 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='portfolio',
            field=models.URLField(blank=True, null=True, verbose_name='Portfolio'),
        ),
    ]
