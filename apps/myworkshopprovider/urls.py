from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from myworkshopprovider.provider import CustomProvider

urlpatterns = default_urlpatterns(CustomProvider)
