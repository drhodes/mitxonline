# Generated by Django 3.1.12 on 2021-09-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_remove_deprecated_profile_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
