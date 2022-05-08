from rest_framework import filters


class TopicsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        id_list = request.query_params.get('topics')
        if not id_list:
            return queryset
        id_list = list(map(int, id_list.split(',')))
        return queryset.filter(topics__id__in=id_list)
