from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, filters
from shared.views import BaseModelViewSet
from .serializers import TopicSerializer
from .models import Topic


@extend_schema_view(
    list=extend_schema(description='Get paginated list of topics.'),
    retrieve=extend_schema(description='Get topic.'),
    create=extend_schema(description='Create topic.'),
    update=extend_schema(description='Update topic.'),
    partial_update=extend_schema(description='Partially update topic.'),
    destroy=extend_schema(description='Delete topic.'),
)
class TopicViewSet(BaseModelViewSet):

    queryset = Topic.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)

    serializer_class = TopicSerializer

    permission_classes_by_action = {
        'create': (permissions.IsAdminUser,),
        'update': (permissions.IsAdminUser,),
        'partial_update': (permissions.IsAdminUser,),
        'destroy': (permissions.IsAdminUser,),
    }
