import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
from django.db import migrations, models
from wagtail.images import get_image_model_string


class Migration(migrations.Migration):

    initial = True

    dependencies = [("wagtailcore", "0040_page_draft_title"), migrations.swappable_dependency(get_image_model_string())]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "description",
                    models.TextField(blank=True, help_text="Briefly describe your event series", max_length=400),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(
                                    help_text="Add optional subheadings between paragraphs, if you're describing the event series in more detail",
                                    label="Optional extra description subheading",
                                    max_length=120,
                                    required=False,
                                ),
                            ),
                            (
                                "paragraph",
                                wagtail.core.blocks.TextBlock(
                                    help_text="Tell people about the event series",
                                    label="Optional extra description text",
                                    required=False,
                                ),
                            ),
                            (
                                "image",
                                wagtail.images.blocks.ImageChooserBlock(
                                    help_text="Add images to describe the event series.",
                                    label="Optional extra event series image(s)",
                                    required=False,
                                ),
                            ),
                            (
                                "quote",
                                wagtail.core.blocks.BlockQuoteBlock(
                                    help_text="Add an inspirational quote!", required=False
                                ),
                            ),
                        ],
                        blank=True,
                        help_text="Add a description of this event or event series.",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=get_image_model_string(),
                    ),
                ),
            ],
            options={"ordering": ["start_date"], "abstract": False,},
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, "wagtailcore.page"),
        ),
        migrations.CreateModel(
            name="EventIndex",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("paginate_by", models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={"abstract": False,},
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, "wagtailcore.page"),
        ),
    ]
