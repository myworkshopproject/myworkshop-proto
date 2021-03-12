from django.apps import AppConfig
from django.utils.translation import ugettext, ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        import accounts.signals.handlers
