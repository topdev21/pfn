# Generated by Django 3.1.6 on 2021-03-27 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0017_auto_20210319_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='id_pk',
            field=models.CharField(blank=1, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='replaytocomment',
            name='id_pk',
            field=models.CharField(blank=1, max_length=8, null=True),
        ),
    ]