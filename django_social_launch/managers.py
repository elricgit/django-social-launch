#Python imports
import logging

#Django imports
from django.contrib.auth.models import User
from django.db import models

#App imports
from . import referrer_url_session_key, referring_user_id_session_key

class SocialLaunchProfileManager(models.Manager):
	def create_from_request(self, user, request):
		referring_user = None
		referrer_url = request.session.get(referrer_url_session_key, '')
		
		referring_user_id = request.session.get(referring_user_id_session_key, None)
		
		if referring_user_id:
			try:
				referring_user = User.objects.get(id=referring_user_id)
			except ValueError:
				pass
			except User.DoesNotExist:
				pass
		
		slp = self.model(
			user=user,
			referrer_url=referrer_url,
			referring_user=referring_user,
		)
		slp.save()
