#Django imports
from django.core.urlresolvers import reverse

#Test imports
from .util  import BaseTestCase

class IndexTestCase(BaseTestCase):
	def test_get(self):
		response = self.client.get(reverse('social_launch_index'))
		
		self.assertEqual(response.status_code, 200)
		



