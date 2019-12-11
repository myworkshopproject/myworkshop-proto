from rest_framework import generics, permissions
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all().prefetch_related("socialaccount_set")
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all().prefetch_related("socialaccount_set")
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
