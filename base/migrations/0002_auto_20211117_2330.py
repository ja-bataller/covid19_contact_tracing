# Generated by Django 3.2.7 on 2021-11-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256)),
                ('gender', models.CharField(max_length=256)),
                ('contact_number', models.CharField(max_length=256)),
                ('email_address', models.EmailField(max_length=256)),
                ('home_address', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
