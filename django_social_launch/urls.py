#Django imports
from django.conf.urls.defaults import *

#App imports
from .views import *

# place app url patterns here
urlpatterns = patterns('',
	url(r'^$', index, name='social_launch_index'),
	url(r'^(?P<referring_user_id>.+)/$', index, name='social_launch_referral'),
)
