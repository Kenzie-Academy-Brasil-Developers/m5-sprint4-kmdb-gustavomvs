# Generated by Django 4.0.6 on 2022-07-06 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='updatedAt',
            new_name='updated_at',
        ),
    ]
