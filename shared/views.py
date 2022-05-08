from rest_framework import viewsets

from shared.mixins import DynamicPermissionsMixin, DynamicSerializersMixin


class BaseModelViewSet(DynamicSerializersMixin, DynamicPermissionsMixin, viewsets.ModelViewSet):
    pass
