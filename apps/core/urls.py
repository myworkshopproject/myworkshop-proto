from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

app_name = "core"


favicon_view = RedirectView.as_view(
    url=settings.STATIC_URL + "core/img/favicon.ico", permanent=True
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),
    path("favicon.ico", favicon_view, name="favicon"),
    path("i18n/", include("django.conf.urls.i18n")),
]
