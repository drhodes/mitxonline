# Generated by Django 3.1.12 on 2021-09-23 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('cms', '0012_product_description_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepage',
            name='feature_image',
            field=models.ForeignKey(blank=True, help_text='Image that will be used where the course is featured or linked. (The recommended dimensions for the image are 375x244)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
