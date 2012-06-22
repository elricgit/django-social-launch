# name copyright (later)

from django.conf.urls.defaults import *
from .views import *

# place app url patterns here
urlpatterns = patterns('',
	url(r'^$', index, name='social_launch_index'),
)
