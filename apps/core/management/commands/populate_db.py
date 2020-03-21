from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from core.models import Workshop


class Command(BaseCommand):
    def _create_site(self):

        example_site = Site.objects.get(pk=1)
        example_site.domain = "127.0.0.1:8000"
        example_site.name = "My Workshop"
        example_site.save()

    def _create_workshop(self):

        example_site = Site.objects.get(pk=1)
        example_workshop = Workshop(site=example_site)
        example_workshop.save()

    def handle(self, *args, **options):
        self._create_site()
        self._create_workshop()
