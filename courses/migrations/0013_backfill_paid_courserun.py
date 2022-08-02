# Generated by Django 3.2.14 on 2022-07-28 20:52

from django.db import migrations


def backfill_paidcourserun(apps, schema_editor):
    """Backfill PaidCourseRun for existing orders"""
    PaidCourseRun = apps.get_model("courses", "PaidCourseRun")
    CourseRun = apps.get_model("courses", "CourseRun")
    Order = apps.get_model("ecommerce", "Order")
    ContentType = apps.get_model("contenttypes", "ContentType")

    for order in Order.objects.filter(state__in=["fulfilled", "review"]):
        # couldn't use order.purchased_runs here from app defined model
        content_type = ContentType.objects.get_for_model(CourseRun)
        for run_obj in order.lines.filter(purchased_content_type=content_type):
            course_run = CourseRun.objects.get(pk=run_obj.purchased_object_id)
            PaidCourseRun.objects.get_or_create(
                order=order, course_run=course_run, user=order.purchaser
            )


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0012_paidcourserun"),
    ]

    operations = [
        migrations.RunPython(backfill_paidcourserun, migrations.RunPython.noop),
    ]
