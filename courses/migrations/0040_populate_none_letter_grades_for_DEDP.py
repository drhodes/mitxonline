# Generated by Django 3.2.18 on 2023-07-27 19:33
from django.db import migrations


def convert_to_letter(grade):
    """Convert a decimal number to letter grade"""
    if grade >= 0.825:
        return "A"
    elif grade >= 0.65:
        return "B"
    elif grade >= 0.55:
        return "C"
    elif grade >= 0.50:
        return "D"
    else:
        return "F"


def populate_letter_grade(apps, schema_editor):
    """Populate letter grades for DEDP courses that were set to None by admin"""
    CourseRunGrade = apps.get_model("courses", "CourseRunGrade")
    course_ids = [
        "course-v1:MITxT+14.100x",
        "course-v1:MITxT+14.750x",
        "course-v1:MITxT+14.740x",
        "course-v1:MITxT+JPAL102x",
        "course-v1:MITxT+14.73x",
        "course-v1:MITxT+14.310x",
        "course-v1:MITxT+14.009x",
    ]
    grades = CourseRunGrade.objects.filter(
        passed=True,
        course_run__course__readable_id__in=course_ids,
        letter_grade=None,
        set_by_admin=True,
    )
    for grade in grades:
        grade.letter_grade = convert_to_letter(grade.grade)
        grade.save()


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0039_program_program_type"),
    ]

    operations = [
        migrations.RunPython(populate_letter_grade, migrations.RunPython.noop),
    ]
