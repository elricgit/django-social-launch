#Django imports
from django.contrib.auth.models import User
from django.test import TestCase

class BaseTestCase(TestCase):
	def setUp(self):
		self.username = 'foo'
		self.password = 'foopw'
		self.user1 = User.objects.create_user(self.username, 'sean@the.jedi', self.password)
	
