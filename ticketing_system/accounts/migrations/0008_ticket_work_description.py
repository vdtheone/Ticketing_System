# Generated by Django 5.0 on 2023-12-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_project_is_blocked"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="work_description",
            field=models.TextField(default="i worked on authentication"),
            preserve_default=False,
        ),
    ]