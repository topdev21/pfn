# Generated by Django 3.1.6 on 2021-03-27 14:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quize', '0005_auto_20210320_0612'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='last_do',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='last do'),
            preserve_default=False,
        ),
    ]