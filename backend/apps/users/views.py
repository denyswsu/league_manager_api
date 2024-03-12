from rest_framework import generics, permissions

from apps.users.serializers import UserMeSerializer


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
