# Generated by Django 3.1.7 on 2021-04-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('student_id', models.CharField(db_index=True, max_length=10)),
                ('organization', models.TextField()),
                ('vpn_ticket', models.TextField()),
                ('at_token', models.TextField()),
                ('user_token', models.UUIDField(db_index=True)),
                ('card_id', models.CharField(db_index=True, max_length=7)),
                ('type', models.IntegerField()),
                ('first_login', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
