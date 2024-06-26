# Generated by Django 5.0.6 on 2024-06-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0007_baseappinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
            ],
        ),
    ]
