# Generated by Django 5.0.6 on 2024-06-02 20:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0005_alter_userprofile_birthdate_delete_usercombineddata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='birthdate',
            new_name='birth_date',
        ),
    ]
