# Generated by Django 3.2.16 on 2023-02-08 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anon', '0008_auto_20230207_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownercampaign',
            name='k',
            field=models.IntegerField(null=True),
        ),
    ]
