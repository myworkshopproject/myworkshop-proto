from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from io import BytesIO
from PIL import Image as Img
from core.models import Image


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

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Image.members_objects.all()
        else:
            return Image.public_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Images"),
            "fontawesome5_class": "far fa-images",
            "short_description": _("All images"),
        }
        return context


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    fields = [
        "picture",
        "title",
        "alt",
        "credit",
        "license",
        "tags",
        "short_description",
        # "exif",
        # "shooted_at",
        # "visibility",
    ]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enctype"] = "multipart/form-data"
        return context


class ImageUpdateView(UpdateView):
    model = Image
    fields = [
        # "picture",
        "title",
        "alt",
        "credit",
        "license",
        "tags",
        "shooted_at",
        "short_description",
    ]
    template_name = "core/forms/object_update.html"
