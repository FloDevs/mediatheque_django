# Generated by Django 5.1.4 on 2025-01-04 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprunt',
            name='date_prevu_retour',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
