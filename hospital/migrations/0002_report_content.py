# Generated by Django 4.1.1 on 2022-10-04 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='content',
            field=models.TextField(default=None),
        ),
    ]