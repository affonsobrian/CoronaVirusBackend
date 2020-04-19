# Generated by Django 3.0.5 on 2020-04-19 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20200418_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('event_run', models.BooleanField(default=False)),
                ('time_run', models.DateTimeField(default=None, null=True)),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.NotificationType')),
            ],
        ),
    ]
