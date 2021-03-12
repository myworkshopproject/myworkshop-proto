from django.contrib.sites.shortcuts import get_current_site
from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAccountAdapter(DefaultAccountAdapter):
    """
    Adapter to enable or disable allauth new signups
    """

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.
        """

        current_site = get_current_site(request)

        if current_site.workshop.is_open_for_signup:
            return True
        else:
            return False
