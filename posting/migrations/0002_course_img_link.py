# Generated by Django 3.1.1 on 2021-01-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='img_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]