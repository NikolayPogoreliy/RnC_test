# Generated by Django 2.2 on 2019-10-10 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libra', '0002_auto_20191010_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookauthor',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_authors', to='libra.Book'),
        ),
    ]
