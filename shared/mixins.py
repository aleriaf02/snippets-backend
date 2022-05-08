from rest_framework import permissions


class DynamicSerializersMixin:
    """
    Allows mapping a specific serializer to each action.

    The mappings are specified in a "serializer_classes_by_action" dictionary.
    """

    serializer_classes_by_action = None

    def get_serializer_class(self):
        if not self.serializer_classes_by_action:
            return self.serializer_class
        return self.serializer_classes_by_action.get(self.action, self.serializer_class)


class DynamicPermissionsMixin:
    """
    Allows mapping a list of permissions to each action.

    The mappings are specified in a "permission_classes_by_action" dictionary.
    """

    permission_classes = (permissions.AllowAny,)
    permission_classes_by_action = {
        'create': permission_classes,
        'list': permission_classes,
        'retrieve': permission_classes,
        'update': permission_classes,
        'partial_update': permission_classes,
        'destroy': permission_classes,
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get(
                    'permission_classes')
            else:
                permission_classes = None

            return [permission() for permission in (permission_classes or self.permission_classes)]
