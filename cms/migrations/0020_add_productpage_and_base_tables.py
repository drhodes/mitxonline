# Generated by Django 3.2.14 on 2022-08-05 16:53

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0016_add_productpage_and_base_tables"),
        ("wagtailcore", "0066_collection_management_permissions"),
        ("wagtailimages", "0023_add_choose_permissions"),
        ("cms", "0019_remove_flexiblepricingrequestform_thank_you_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgramIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="ProgramPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "description",
                    wagtail.core.fields.RichTextField(
                        help_text="The description shown on the home page and product page. The recommended character limit is 1000 characters. Longer entries may not display nicely on the page."
                    ),
                ),
                (
                    "length",
                    models.CharField(
                        default="",
                        help_text="A short description indicating how long it takes to complete (e.g. '4 weeks').",
                        max_length=50,
                    ),
                ),
                (
                    "effort",
                    models.CharField(
                        blank=True,
                        help_text="A short description indicating how much effort is required (e.g. 1-3 hours per week).",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "price",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "price_details",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            wagtail.core.blocks.CharBlock(
                                                help="Displayed over the product detail page under the price tile.",
                                                max_length=150,
                                            ),
                                        ),
                                        (
                                            "link",
                                            wagtail.core.blocks.URLBlock(
                                                help="Specify the URL to redirect the user for the product's price details page.",
                                                required=False,
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        help_text="Specify the product price details.",
                    ),
                ),
                (
                    "prerequisites",
                    wagtail.core.fields.RichTextField(
                        blank=True,
                        help_text="A short description indicating prerequisites of this course.",
                        null=True,
                    ),
                ),
                (
                    "about",
                    wagtail.core.fields.RichTextField(
                        blank=True, help_text="About this course details.", null=True
                    ),
                ),
                (
                    "video_url",
                    models.URLField(
                        blank=True,
                        help_text="URL to the video to be displayed for this program/course. It can be an HLS or Youtube video URL.",
                        null=True,
                    ),
                ),
                (
                    "what_you_learn",
                    wagtail.core.fields.RichTextField(
                        blank=True,
                        help_text="What you will learn from this course.",
                        null=True,
                    ),
                ),
                (
                    "faculty_section_title",
                    models.CharField(
                        blank=True,
                        default="Meet your instructors",
                        help_text="The title text to display in the faculty cards section of the product page.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "faculty_members",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "faculty_member",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "name",
                                            wagtail.core.blocks.CharBlock(
                                                help_text="Name of the faculty member.",
                                                max_length=100,
                                            ),
                                        ),
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                help_text="Profile image size must be at least 300x300 pixels."
                                            ),
                                        ),
                                        (
                                            "description",
                                            wagtail.core.blocks.RichTextBlock(
                                                help_text="A brief description about the faculty member."
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                        help_text="The faculty members to display on this page",
                        null=True,
                    ),
                ),
                (
                    "feature_image",
                    models.ForeignKey(
                        help_text="Image that will be used where the course is featured or linked. (The recommended dimensions for the image are 375x244)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "program",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="page",
                        to="courses.program",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
