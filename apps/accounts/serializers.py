from django.conf import settings
from rest_framework import serializers
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    def to_representation(self, obj):
        user = super().to_representation(obj)
        try:
            socialaccount = obj.socialaccount_set.all()[0]
            oauth_server_baseurl = settings.OAUTH_SERVER_BASEURL
            user["maker_url"] = "{}/api/v1/makers/{}/".format(
                oauth_server_baseurl, socialaccount.uid
            )
        except:
            pass

        return user

    class Meta:
        model = CustomUser
        fields = ["url", "id", "username", "first_name", "last_name"]
