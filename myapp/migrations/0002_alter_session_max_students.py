# Generated by Django 4.1.5 on 2023-05-03 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="max_students",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
