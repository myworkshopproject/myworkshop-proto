# Publications App
from django.utils.translation import ugettext_lazy as _

PUBLICATIONS_ID_LENGHT = 6

PUBLICATIONS_PUBLICATION_ICON = "fas fa-pencil-alt"
PUBLICATIONS_PUBLICATIONS_ICON = "fas fa-photo-video"
PUBLICATIONS_ARTICLE_ICON = "far fa-newspaper"
PUBLICATIONS_TUTORIAL_ICON = "fas fa-shoe-prints"
PUBLICATIONS_IMAGE_ICON = "far fa-image"
PUBLICATIONS_MANUAL_ICON = "fas fa-book"
PUBLICATIONS_TOOL_ICON = "fas fa-tools"
PUBLICATIONS_VIDEO_ICON = "fas fa-film"
PUBLICATIONS_GALLERY_ICON = "far fa-images"

PUBLICATIONS_DEFAULT_ARTICLE_TITLE = _("New article title")
PUBLICATIONS_DEFAULT_ARTICLE_DESCRIPTION = _("A short description...")
PUBLICATIONS_DEFAULT_ARTICLE_TEXT = _(
    """## First paragraph
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor...
"""
)

PUBLICATIONS_DEFAULT_TUTORIAL_TITLE = _("New tutorial title")
PUBLICATIONS_DEFAULT_TUTORIAL_DESCRIPTION = _("A short description...")
PUBLICATIONS_DEFAULT_TUTORIAL_DIFFICULTY = 1
PUBLICATIONS_DEFAULT_TUTORIAL_DURATION = _("45 min")
PUBLICATIONS_DEFAULT_TUTORIAL_COST = _("10 €")
PUBLICATIONS_DEFAULT_TUTORIAL_TEXT = _(
    """## First step
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor...
"""
)

PUBLICATIONS_DEFAULT_IMAGE_TITLE = _("New image title")
PUBLICATIONS_DEFAULT_IMAGE_DESCRIPTION = _("A short caption...")
