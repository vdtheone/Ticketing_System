# Generated by Django 5.0 on 2023-12-25 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0011_remove_ticket_comment_ticket_work_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="work_description",
        ),
        migrations.AddField(
            model_name="ticket",
            name="comment",
            field=models.TextField(default="dlskfjd"),
            preserve_default=False,
        ),
    ]