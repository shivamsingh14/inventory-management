from rest_framework import viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from app.libs.permissions import StaffPermissions, OwnerPermission
from app.stores.models import Box, User
from app.stores.serializers import BoxSerializer, FullBoxSerializer, UserSerializer
from app.libs.filter_backend import CreatorFilterBackend
from app.libs.utils import CheckConstraintsUtil

class BoxFilter(django_filters.FilterSet):
	class Meta:

		model = Box
		fields = {
			'length': ['gte', 'lte'],
			'breadth': ['gte', 'lte'],
			'height': ['gte', 'lte'],
			'area': ['gte', 'lte'],
			'user__username': ['iexact'],
			'created_at': ['gte']
		}
class BoxViewSet(viewsets.ModelViewSet):
	"""
	the viewset handles creation, list, updation and deletion operation on Box model
	"""
	filter_backends = (DjangoFilterBackend,)
	filter_class = BoxFilter
	queryset = Box.objects.all()

	def get_permissions(self):
		"""
		overridden permisison classes to support staff permissions while creating, updating box
		and support owner permission while deleting box
		"""
		if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
			self.permission_classes.append(StaffPermissions)
		
		if self.request.method == "DELETE":
			self.permission_classes.append(OwnerPermission)

		return super(BoxViewSet, self).get_permissions()

	def get_serializer_class(self):
		"""
		overridden serializer class to provide full serialization for staff users 
		and basic serialization for other users
		"""
		if self.request.user.is_staff:
			return FullBoxSerializer
		return BoxSerializer

	def perform_destroy(self, instance):
		"""
		overridden delete method inorder to check area and volume constraints before deleting
		"""
		user = self.request.user
		check_constraint_util = CheckConstraintsUtil(user, validated_data=None, instance=instance) 
		check_constraint_util.check_constraints()
		return super(BoxViewSet, self).perform_destroy(instance)

class MyBoxViewSet(BoxViewSet):
	"""
	the viewset handles list of my boxes
	"""
	permission_classes = [IsAuthenticated, StaffPermissions]
	filter_backends = (CreatorFilterBackend, DjangoFilterBackend)

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

	permission_classes = [AllowAny, ]
	serializer_class = UserSerializer



