# Generated by Django 5.0 on 2023-12-25 18:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0008_ticket_work_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="work_description",
            new_name="work_description",
        ),
    ]
