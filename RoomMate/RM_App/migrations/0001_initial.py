# Generated by Django 4.2.11 on 2025-03-31 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('user_email', models.CharField(max_length=64)),
                ('user_password', models.CharField(max_length=64)),
            ],
        ),
    ]
