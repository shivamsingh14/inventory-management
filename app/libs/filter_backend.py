from rest_framework import filters

class CreatorFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own boxes.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)
