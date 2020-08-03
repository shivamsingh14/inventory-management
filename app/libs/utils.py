from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Sum
from django.utils import timezone

from app.libs.constants import ERROR_MESSAGES, THRESHOLD_VALUES
from app.stores.models import Box

from datetime import timedelta

class CheckConstraintsUtil(object):

	def __init__(self, user, validated_data=None, instance=None):

		self.instance = instance
		self.user = user
		self.validated_data = validated_data
		self.last_week = timezone.now() - timedelta(days=7)

	def check_constraints(self):
		"""
		function to check all the constraints while creating, updating or deleting boxes
		"""
		if self.validated_data is not None:
			self.length = self.validated_data['length'] if self.validated_data.get('length') else instance.length
			self.breadth = self.validated_data['breadth'] if self.validated_data.get('breadth') else instance.breadth
			self.height = self.validated_data['height'] if self.validated_data.get('height') else instance.height

		self.check_area()
		self.check_volume_by_user()

		if self.instance is None: # needs to be checked only while adding new boxes
			self.check_boxes_added_in_week()
			self.check_boxes_added_in_week_by_user()

		return self.validated_data

	def check_area(self):
		"""
		function to check that maximum average is maintained while creating, updating or deleting boxes
		"""
		old_area = 0
		new_area = 0
		area_sum = 0
		area_sum_count_dict = Box.objects.aggregate(sum=Sum('area'), count=Count('area'))
		area_sum = area_sum_count_dict.get('sum') if area_sum_count_dict.get('sum') is not None else 0 
		count = area_sum_count_dict['count']

		if self.validated_data is not None:
			count = area_sum_count_dict['count'] + 1
			new_area = 2 * ((self.length * self.breadth) + (self.height * self.breadth) + (self.length * self.height))

		if self.instance:
			old_area = self.instance.area
			count = count - 1
		
		area_average = (area_sum + new_area - old_area) / count
		if area_average > THRESHOLD_VALUES['AREA']:
			raise ValidationError(ERROR_MESSAGES['AVERAGE_AREA_MAX_REACHED'])

	def check_volume_by_user(self):
		"""
		function to check that maximum volume added by a user is maintained while creating, updating or deleting boxes
		"""
		old_volume = 0
		new_volume = 0
		volume_sum_count_dict = Box.objects.filter(user=self.user).aggregate(sum=Sum('volume'), count=Count('volume'))
		volume_sum = volume_sum_count_dict.get('sum') if volume_sum_count_dict.get('sum') is not None else 0
		count = volume_sum_count_dict['count']

		if self.validated_data is not None:
			count = volume_sum_count_dict['count'] + 1
			new_volume = self.length * self.breadth * self.height

		if self.instance:
			old_volume = self.instance.volume
			count = count - 1

		volume_average = (volume_sum + new_volume - old_volume) / count
		if volume_average > THRESHOLD_VALUES['VOLUME_ADDED_BY_USER']:
			raise ValidationError(ERROR_MESSAGES['AVERAGE_VOLUME_MAX_REACHED'])

	def check_boxes_added_in_week(self):
		"""
		function to check that maximum boxes added i a week is maintained while creating, updating or deleting boxes
		"""
		box_added_this_week = Box.objects.filter(created_at__gte=self.last_week).count()
		if box_added_this_week > THRESHOLD_VALUES['TOTAL_BOXES_ADDED_IN_WEEK']:
			raise ValidationError(ERROR_MESSAGES['BOX_ADDED_THIS_WEEK_MAX_REACHED'])

	def check_boxes_added_in_week_by_user(self):
		"""
		function to check that maximum volume added by a user in a week is maintained while creating, updating or deleting boxes
		"""
		box_added_this_week_user = Box.objects.filter(created_at__gte=self.last_week, user=self.user).count()
		if box_added_this_week_user > THRESHOLD_VALUES['TOTAL_BOXES_ADDED_IN_WEEK_BY_USER']:
			raise ValidationError(ERROR_MESSAGES['BOX_ADDED_THIS_WEEK_MAX_REACHED_BY_USER'])
