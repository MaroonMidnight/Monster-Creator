# Generated by Django 5.1.2 on 2024-11-04 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_moves_alter_monster_passive_monster_moves'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moves',
            old_name='move_description',
            new_name='move_effect',
        ),
    ]
