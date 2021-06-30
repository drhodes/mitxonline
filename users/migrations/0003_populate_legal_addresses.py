# Generated by Django 2.1.7 on 2019-04-22 15:24

from django.db import migrations


def add_legal_addresses(apps, schema_editor):
    User = apps.get_model("users", "User")
    LegalAddress = apps.get_model("users", "LegalAddress")

    for user in User.objects.all().iterator():
        LegalAddress.objects.create(user=user)


def remove_legal_addresses(apps, schema_editor):
    LegalAddress = apps.get_model("users", "LegalAddress")
    LegalAddress.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("users", "0002_add_legal_address")]

    operations = [migrations.RunPython(add_legal_addresses, remove_legal_addresses)]
