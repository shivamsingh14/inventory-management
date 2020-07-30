from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.libs.permissions import StaffPermissions
from app.stores.models import Box
from app.stores.serializers import BoxSerializer

class BoxViewSet(viewsets.ModelViewSet):

    """
    the viewset handles creation, list, updation and deletion operation on Box model
    """
    permission_classes = (IsAuthenticated, StaffPermissions, )
    serializer_class = BoxSerializer

    queryset = Box.objects.all()

