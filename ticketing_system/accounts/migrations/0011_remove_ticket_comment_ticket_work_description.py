# Generated by Django 5.0 on 2023-12-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_rename_work_description_ticket_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="work_description",
        ),
        migrations.AddField(
            model_name="ticket",
            name="work_description",
            field=models.TextField(default="dkslaj"),
            preserve_default=False,
        ),
    ]
