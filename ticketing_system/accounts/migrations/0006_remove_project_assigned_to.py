# Generated by Django 5.0 on 2023-12-24 16:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_project_assigned_to"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="assigned_to",
        ),
    ]
