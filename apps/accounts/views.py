from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from allauth.account.decorators import verified_email_required
from accounts.models import CustomUser


class CustomUserDetailView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/user_detail.html"


class CustomUserListView(ListView):
    model = CustomUser
    template_name = "accounts/user_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(username="deleted").exclude(username="deleted")
