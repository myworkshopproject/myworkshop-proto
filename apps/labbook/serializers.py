from rest_framework import serializers
from labbook.models import Entry, Image, Note


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:image-detail")

    def to_representation(self, obj):
        image = super().to_representation(obj)
        image["type"] = "image"
        return image

    class Meta:
        model = Image
        fields = [
            "url",
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "picture",
            "caption",
        ]


class NoteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:note-detail")

    def to_representation(self, obj):
        note = super().to_representation(obj)
        note["type"] = "note"
        return note

    class Meta:
        model = Note
        fields = ["url", "id", "created_by", "created_at", "updated_at", "body"]


class EntrySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        if hasattr(obj, "note"):
            return NoteSerializer(obj, context=self.context).to_representation(obj.note)

        if hasattr(obj, "image"):
            return ImageSerializer(obj, context=self.context).to_representation(
                obj.image
            )

        return super(EntrySerializer, self).to_representation(obj)

    class Meta:
        model = Entry
        fields = ["id", "created_by", "created_at", "updated_at"]
