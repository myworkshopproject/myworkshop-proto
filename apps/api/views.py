from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse_lazy("api:user-list", request=request, format=format),
            "entries": reverse_lazy("api:entry-list", request=request, format=format),
            "images": reverse_lazy("api:image-list", request=request, format=format),
            "notes": reverse_lazy("api:note-list", request=request, format=format),
            "projects": reverse_lazy(
                "api:project-list", request=request, format=format
            ),
        }
    )
