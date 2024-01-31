# Generated by Django 4.2.9 on 2024-01-18 12:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('influencers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofile',
            name='url_profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='baseprofile',
            unique_together={('user', 'url_profile')},
        ),
    ]
