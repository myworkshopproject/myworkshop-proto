from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    def _create_site(self):

        example_site = Site.objects.get(pk=1)
        example_site.domain = "127.0.0.1:8000"
        example_site.name = "My Workshop"
        example_site.save()

    def handle(self, *args, **options):
        self._create_site()
