from markdown import Markdown
from markdown.extensions.toc import TocExtension
from random import choice
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from publications.models import BaseModel

DEFAULT_SOURCE_TEXT = """title: Choose a good title
description: Write a short description.

## First paragraph
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor...
"""


class Publication(BaseModel):
    history = HistoricalRecords()

    id = models.CharField(
        primary_key=True, max_length=settings.PUBLICATIONSAPP_ID_LENGHT, editable=False
    )

    source = models.TextField(
        blank=True,
        verbose_name=_("source"),
        help_text=_("You can use Markdown syntax."),
        default=DEFAULT_SOURCE_TEXT,
    )
    toc = models.TextField(blank=True, editable=False)
    html = models.TextField(blank=True, editable=False)

    @property
    def title(self):
        if "title" in self.metadata:
            title = self.metadata["title"][0]
            if title:
                return title
        return _("untitled")

    @property
    def description(self):
        if "description" in self.metadata:
            description = self.metadata["description"][0]
            if description:
                words = description.split(" ")
                lead_max_word_number = 25
                if len(words) <= lead_max_word_number:
                    return description
                else:
                    return " ".join(words[:lead_max_word_number]) + "..."
        return _("No description.")

    @property
    def tags(self):
        if "tag" in self.metadata:
            return self.metadata["tag"]
        return []

    @property
    def icon(self):
        return "fas fa-feather-alt"

    class Meta(BaseModel.Meta):
        verbose_name = _("publication")
        verbose_name_plural = _("publications")

    def get_absolute_url(self):
        return reverse("publications:publication-detail", args=[str(self.id)])

    def get_update_url(self):
        return reverse("publications:publication-update", args=[str(self.id)])

    def get_delete_url(self):
        return reverse("publications:publication-delete", args=[str(self.id)])

    def get_cancel_url(self):
        return self.get_absolute_url()

    def save(self, *args, **kwargs):
        ALL_EXCLUDE_SIMILAR = (
            "23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"  # 57
        )
        LETTERS_EXCLUDE_SIMILAR = (
            "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"  # 49
        )

        if not self.id:
            is_unique = False
            while not is_unique:
                id = "".join(
                    [choice(LETTERS_EXCLUDE_SIMILAR)]
                    + [
                        choice(ALL_EXCLUDE_SIMILAR)
                        for i in range(settings.PUBLICATIONSAPP_ID_LENGHT - 1)
                    ]
                )
                is_unique = not Publication.objects.filter(id=id).exists()
            self.id = id

        try:
            md = Markdown(
                extensions=[
                    # "abbr",
                    "fenced_code",
                    # "footnotes",
                    "tables",
                    # "extra",
                    # "admonition",
                    # "codehilite",
                    "meta",
                    TocExtension(
                        # title=None,
                        # anchorlink=True,
                        # anchorlink_class="toclink",
                        permalink=True,
                        # permalink_class="headerlink",
                        permalink_class="ml-1 has-text-grey-lighter",
                        # permalink_title="Permanent link",
                        # baselevel=1,
                        baselevel=2,
                        toc_depth="3-4",
                    ),
                ],
                output_format="html5",
            )
            self.html = md.convert(self.source)
            self.metadata = md.Meta
            self.toc = md.toc

        except:
            self.html = ""
            self.metadata = {}
            self.toc = ""

        super(Publication, self).save(*args, **kwargs)
