from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import make_password, check_password

from app.stores.models import Box, User
from app.libs.utils import CheckConstraintsUtil


class UserSerializer(serializers.ModelSerializer):
	"""
	User model Signup Serializer
	"""
	token = serializers.CharField(read_only=True)
	password = serializers.CharField(write_only=True, style={'input_type': 'passsword'})

	class Meta(object):
		model = User
		fields = ('id', 'first_name', 'last_name', 'username', 'gender', 'email', 'is_staff', 'token', 'password')
		read_only_fields = ('id',)

	def validate(self, data):
		"""
		override user serializer to hash passwoed before saving user
		"""
		if self.instance:
			return super(UserSerializer, self).validate(data)
		else:
			user = User(username=data['username'])
			data['password'] = make_password(data['password'])
			return data

	def create(self, validated_data):
		"""
		overriding default create to insert token
		"""
		instance = super(UserSerializer, self).create(validated_data)
		instance.set_password(validated_data['password'])
		token = Token.objects.create(user=instance)
		instance.token = token
		return instance

class BoxSerializer(serializers.ModelSerializer):
	"""
	Creation and list Viewsets serializer for Box model
	"""
	class Meta(object):
		model = Box
		fields = ('id', 'length', 'breadth', 'height', 'area', 'volume')
		read_only_fields = ('id', 'area', 'volume')

	def validate(self, data):
		"""
		overriden validate to check the constraints while adding the box
		"""
		validated_data = super(BoxSerializer, self).validate(data)
		user = self.context['request'].user
		check_constraint_util = CheckConstraintsUtil(user, validated_data, self.instance) 
		return check_constraint_util.check_constraints()
class FullBoxSerializer(BoxSerializer):
	"""
	Creation and list Viewsets serializer for Box model for staff users
	"""
	created_by = UserSerializer(source="user", read_only=True)
	class Meta(object):
		model = Box
		fields = BoxSerializer.Meta.fields + ('created_by', 'updated_at')
		read_only_fields = BoxSerializer.Meta.read_only_fields + ('updated_at',)

	def create(self, validated_data):
		"""
		overridden create method to add the requesting user while creating box
		"""
		validated_data['user'] = self.context['request'].user
		return super(FullBoxSerializer, self).create(validated_data)

