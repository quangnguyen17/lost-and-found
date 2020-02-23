# Generated by Django 3.0.3 on 2020-02-23 01:03

from django.db import migrations, models
import django.db.models.deletion
import login_n_registration_app.models
import lost_n_found_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_n_registration_app', '0008_auto_20200222_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('desc', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=lost_n_found_app.models.path_and_rename)),
                ('found', models.BooleanField(default=False)),
                ('campus', models.CharField(choices=[(login_n_registration_app.models.Campus['arlington'], 'Arlington, VA'), (login_n_registration_app.models.Campus['boise'], 'Boise, ID'), (login_n_registration_app.models.Campus['chicago'], 'Chicago, IL'), (login_n_registration_app.models.Campus['dallas'], 'Dallas, TX'), (login_n_registration_app.models.Campus['los_angeles'], 'Los Angeles, CA'), (login_n_registration_app.models.Campus['oakland'], 'Oakland, CA'), (login_n_registration_app.models.Campus['orange_county'], 'Orange County, CA'), (login_n_registration_app.models.Campus['seatle'], 'Seatle, WA'), (login_n_registration_app.models.Campus['silicon_valley'], 'Silicon Valley, CA'), (login_n_registration_app.models.Campus['tulsa'], 'Tulsa, OK')], max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('found_by_whom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='found_items', to='login_n_registration_app.User')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='login_n_registration_app.User')),
            ],
        ),
    ]
