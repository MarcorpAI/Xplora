# Generated by Django 5.0.3 on 2024-05-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HS', '0007_documentupload_file_metadata_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentupload',
            name='file_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
