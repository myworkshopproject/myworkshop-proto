import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from django.conf import settings
from myworkshopprovider.provider import CustomProvider


class CustomAdapter(OAuth2Adapter):
    provider_id = CustomProvider.id

    oauth_server_baseurl = settings.OAUTH_SERVER_BASEURL
    access_token_url = "{}/o/token/".format(oauth_server_baseurl)
    authorize_url = "{}/o/authorize/".format(oauth_server_baseurl)
    profile_url = "{}/accounts/profile/".format(oauth_server_baseurl)

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        ### attention : prévoir un test !!!!!
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)
