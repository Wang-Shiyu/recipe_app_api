from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # When this viewset is invoked from a URL, it will call get_queryset to
    # retrieve objects specified by queryset, we can apply custom filter here
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # the request will be passed into the self as a class variable and
        # the user should be assigned to that request(authentication required)
        return self.queryset.filter(user=self.request.user).order_by('-name')
