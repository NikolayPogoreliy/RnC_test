# Generated by Django 2.2 on 2019-10-11 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libra', '0003_auto_20191010_1147'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('first_name', 'last_name', 'birth_date')},
        ),
    ]
