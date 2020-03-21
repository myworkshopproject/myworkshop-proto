from django.http import HttpResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from core.models import Image
from PIL import Image as Img
from io import BytesIO


class ImageThumbnailView(View):
    def get(self, request, *args, **kwargs):
        try:
            picture = Image.objects.get(pk=kwargs["pk"]).picture
            image = Img.open(picture)
            image.thumbnail((200, 200), Img.ANTIALIAS)
            byte_file = BytesIO()
            image.save(byte_file, format=image.format)
            image_data = byte_file.getvalue()
            mime_type = Img.MIME[image.format]
            return HttpResponse(image_data, content_type=mime_type)
        except:
            return HttpResponse("")


class ImageDetailView(DetailView):
    # TO-DO
    # filtrer les images publiques / privées
    model = Image
    context_object_name = "image"
    template_name = "core/image_detail.html"


class ImageListView(ListView):
    model = Image
    template_name = "core/image_list.html"
