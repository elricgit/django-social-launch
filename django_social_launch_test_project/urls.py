from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	
	url(r'^accounts/', include('registration.backends.default.urls')),			# changed to url for consistancy??? and updated for registration deprecation
<<<<<<< HEAD
=======
	url(r'', include('social_auth.urls')),
>>>>>>> b78e863fc11a8645ff4a499a5876b1b1685f37fe
	url(r'^', include('django_social_launch.urls')),
)
