# Generated by Django 4.2.9 on 2024-01-16 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('influencers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile_pictures', models.ImageField(blank=True, null=True, upload_to='influencers/profile_images')),
                ('profile_pictures_url', models.TextField(blank=True, null=True)),
                ('followers', models.IntegerField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='influencers.baseprofile')),
            ],
        ),
    ]
