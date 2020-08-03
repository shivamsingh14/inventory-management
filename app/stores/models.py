from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from app.libs.constants import MAX_LENGTH_DICT 

class User(AbstractUser):
	"""
	User model to store user's attributes
	"""
	MALE = 'M'
	FEMALE = 'F'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female')
	)

	gender = models.CharField(choices=GENDER_CHOICES, max_length=MAX_LENGTH_DICT["SMALL"], default='M')
	class Meta:
		db_table = 'User'

class Box(models.Model):
	"""
	Box model to store cuboid's attributes
	"""
	length = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
	breadth = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
	height = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
	area = models.DecimalField(max_digits=15, decimal_places=2)
	volume = models.DecimalField(max_digits=15, decimal_places=2)
	user = models.ForeignKey(User, related_name="boxes", on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'Box'
		verbose_name = 'Box'
		verbose_name_plural = 'Boxes'

	def save(self, *args, **kwargs):
		"""
		override default save model to compute area and volume before storing in database
		"""
		self.area = 2 * ((self.length * self.breadth) + (self.height * self.breadth) + (self.length * self.height))
		self.volume = self.length*self.breadth*self.height
		return super(Box, self).save(*args, **kwargs)
 