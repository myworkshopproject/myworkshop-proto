from django.urls import include, path
from api.views import api_root
from accounts.views import CustomUserList, CustomUserDetail
from labbook.views import EntryList, NoteList, NoteDetail, ImageList, ImageDetail
from projects.views import ProjectList, ProjectDetail

app_name = "api"


urlpatterns = [
    path("", api_root, name="root"),
    path("users/", CustomUserList.as_view(), name="user-list"),
    path("users/<uuid:pk>/", CustomUserDetail.as_view(), name="user-detail"),
    path("entries/", EntryList.as_view(), name="entry-list"),
    path("notes/", NoteList.as_view(), name="note-list"),
    path("notes/<uuid:pk>/", NoteDetail.as_view(), name="note-detail"),
    path("images/", ImageList.as_view(), name="image-list"),
    path("images/<uuid:pk>/", ImageDetail.as_view(), name="image-detail"),
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<uuid:pk>/", ProjectDetail.as_view(), name="project-detail"),
]
