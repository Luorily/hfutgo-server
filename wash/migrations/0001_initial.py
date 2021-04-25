# Generated by Django 3.1.7 on 2021-04-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None)),
                ('sort', models.IntegerField(default=None)),
                ('campus', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None)),
                ('building', models.TextField(default=None)),
                ('type', models.IntegerField(default=None)),
                ('sort', models.IntegerField(default=None)),
                ('NQT', models.TextField(default=None)),
                ('machineid', models.TextField(default=None)),
            ],
        ),
    ]
