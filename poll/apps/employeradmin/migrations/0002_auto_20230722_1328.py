# Generated by Django 3.1 on 2023-07-22 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeradmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmaster',
            name='event_title',
            field=models.TextField(null=True),
        ),
    ]
