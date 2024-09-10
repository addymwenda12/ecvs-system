# Generated by Django 5.1.1 on 2024-09-10 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecvs', '0003_credential_ipfs_hash_credential_private_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credential',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='credential',
            name='ipfs_hash',
        ),
        migrations.AlterField(
            model_name='credential',
            name='degree',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='credential',
            name='institution',
            field=models.CharField(max_length=200),
        ),
    ]
