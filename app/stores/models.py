from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from app.libs.constants import MAX_LENGTH_DICT 

class User(AbstractBaseUser, PermissionsMixin):


		"""
		User model to store user's attributes
		"""

		MALE = 'M'
		FEMALE = 'F'

		GENDER_CHOICES = (
				(MALE, 'Male'),
				(FEMALE, 'Female')
		)

		name = models.CharField(max_length=MAX_LENGTH_DICT["NAME"])
		email = models.EmailField(max_length=MAX_LENGTH_DICT["EMAIL"], unique=True)
		is_staff = models.BooleanField(default=False)
		gender = models.CharField(choices=GENDER_CHOICES, max_length=MAX_LENGTH_DICT["SMALL"], default='M')

		created_at = models.DateTimeField(auto_now_add=True)
		updated_at = models.DateTimeField(auto_now=True)

		USERNAME_FIELD = 'email'

		class Meta:
			db_table = 'User'
			verbose_name = 'User'

class Box(models.Model):

		"""
		Box model to store cuboid's attributes
		"""

		length = models.IntegerField()
		breadth = models.IntegerField()
		height = models.IntegerField()

		created_at = models.DateTimeField(auto_now_add=True)
		updated_at = models.DateTimeField(auto_now=True)

		class Meta:
			db_table = 'Box'
			verbose_name = 'Box'
			verbose_name_plural = 'Boxes'
