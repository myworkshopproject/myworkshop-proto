from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def get_publication_to_context(request):
    return {
        "publication_create_menu": {
            "title": _("New publication"),
            "icon": settings.PUBLICATIONS_PUBLICATION_ICON,
            "items": [
                {
                    "url": reverse("publications:article-create"),
                    "icon": settings.PUBLICATIONS_ARTICLE_ICON,
                    "text": _("Article"),
                },
                {
                    "url": reverse("publications:tutorial-create"),
                    "icon": settings.PUBLICATIONS_TUTORIAL_ICON,
                    "text": _("Tutorial"),
                },
                {
                    "url": reverse("publications:image-create"),
                    "icon": settings.PUBLICATIONS_IMAGE_ICON,
                    "text": _("Image"),
                },
            ],
        },
        "publication_menu": {
            "title": _("Publication"),
            "icon": settings.PUBLICATIONS_PUBLICATION_ICON,
            "items": [
                {
                    "url": reverse("publications:publication-list") + "?type=article",
                    "icon": settings.PUBLICATIONS_ARTICLE_ICON,
                    "text": _("Articles"),
                },
                {
                    "url": reverse("publications:publication-list") + "?type=tutorial",
                    "icon": settings.PUBLICATIONS_TUTORIAL_ICON,
                    "text": _("Tutorials"),
                },
                {
                    "url": reverse("publications:publication-list") + "?type=image",
                    "icon": settings.PUBLICATIONS_IMAGE_ICON,
                    "text": _("Images"),
                },
                {
                    "url": reverse("publications:publication-list"),
                    "icon": settings.PUBLICATIONS_PUBLICATIONS_ICON,
                    "text": _("All publications"),
                },
            ],
        },
    }
