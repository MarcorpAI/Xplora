# Generated by Django 5.0.3 on 2024-04-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentupload',
            name='file_content',
            field=models.FileField(upload_to='chromadb.sqlite3'),
        ),
    ]
