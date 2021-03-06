#Django imports
from django.contrib.auth.models import User
from django.db import models

#App imports
from .managers import SocialLaunchProfileManager

# Create your models here.

class SocialLaunchProfile(models.Model):
	objects = SocialLaunchProfileManager()
	
	user				= models.OneToOneField(User)
	referrer_url		= models.CharField(blank=True, max_length=255)
	referring_user		= models.ForeignKey(User, null=True, related_name='referred_profile_set')

	def __unicode__(self):
		return unicode(self.user)
