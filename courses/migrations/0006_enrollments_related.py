# Generated by Django 3.1.12 on 2021-09-27 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_add_help_text_in_courserun_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courserunenrollment",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                to="courses.courserun",
            ),
        ),
    ]
