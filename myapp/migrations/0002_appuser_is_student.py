# Generated by Django 4.1.5 on 2023-05-03 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="is_student",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]