from markdown import Markdown
from markdown.extensions.toc import TocExtension
from random import choice
from urllib.parse import urlparse
from django.conf import settings
from django.db import models
from django.urls import resolve, reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from model_utils.managers import InheritanceManager
from simple_history.models import HistoricalRecords
from publications.models import BaseModel


class Publication(BaseModel):
    history = HistoricalRecords()

    id = models.CharField(
        primary_key=True, max_length=settings.PUBLICATIONS_ID_LENGHT, editable=False
    )

    source = models.TextField(
        blank=True,
        verbose_name=_("source"),
        help_text=_("You can use Markdown syntax."),
    )
    toc = models.TextField(blank=True, editable=False)
    html = models.TextField(blank=True, editable=False)

    objects = InheritanceManager()

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
        return settings.PUBLICATIONS_PUBLICATION_ICON

    @property
    def featured_image(self):
        if "image" in self.metadata:
            featured_image = self.metadata["image"][0]
            try:
                from publications.models import Image

                url = urlparse(featured_image)
                match = resolve(url.path)
                pk = match.kwargs["pk"]

                return Image.objects.get(pk=pk)
            except:
                return None
        return None

    class Meta(BaseModel.Meta):
        verbose_name = _("publication")
        verbose_name_plural = _("publications")

    def get_absolute_url(self):
        return reverse("publications:publication-detail", args=[str(self.id)])

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
                        for i in range(settings.PUBLICATIONS_ID_LENGHT - 1)
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
