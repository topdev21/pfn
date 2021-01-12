# Generated by Django 3.1.1 on 2021-01-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0007_auto_20210107_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentaire',
            options={'ordering': ['-at']},
        ),
        migrations.AddField(
            model_name='course',
            name='also_send',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='mail_send',
            field=models.BooleanField(default=False),
        ),
    ]
