from rest_framework import serializers
from labbook.models import Image
from labbook.serializers import ImageSerializer
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:project-detail")
    featured_image = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=False,
        view_name="api:image-detail",
        queryset=Image.objects.all(),
    )

    class Meta:
        model = Project
        fields = "__all__"
