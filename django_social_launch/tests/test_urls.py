#Django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sessions.backends.db import SessionStore

#App imports
from .. import user_successfully_created_msg, referrer_url_session_key, referring_user_id_session_key
from ..models import SocialLaunchProfile

#Test imports
from .util import BaseTestCase

class IndexTestCase(BaseTestCase):
	def test_get(self):
		response = self.client.get(reverse('social_launch_index'))
		
		self.assertEqual(response.status_code, 200)
		
	def test_get_with_referrer(self):
		referrer_url = 'http://facebook.com'
		response = self.client.get(reverse('social_launch_index'), HTTP_REFERER=referrer_url)
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.client.session[referrer_url_session_key], referrer_url)
		
	def test_post_success_creates_new_user(self):
		post_data = {'email' : 'foo@example.com'}
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_index'), post_data, follow=True)
		
		users = User.objects.all()
		slps = SocialLaunchProfile.objects.all()
		
		self.assertEquals(len(users), 2)
		self.assertEquals(len(slps), 1)
		
		user = users[1]
		slp = slps[0]
		
		self.assertRedirects(response, reverse('social_launch_referral', kwargs={'referring_user_id' : user.id}))
		
		self.assertEquals(user.email, post_data['email'])
		self.assertEquals(user.username, post_data['email'])
		self.assertFalse(user.has_usable_password())
		self.assertContains(response, user_successfully_created_msg)
		self.assertEquals(slp.user, user)
		self.assertEquals(slp.referrer_url, '')
		self.assertEquals(slp.referring_user, None)
		
	def test_post_success_creates_new_user_with_referrer(self):
		referrer_url = 'http://facebook.com'
		
		post_data = {'email' : 'foo@example.com'}
		
		session = SessionStore()
		session[referrer_url_session_key] = referrer_url
		session[referring_user_id_session_key] = ''
		session.save()
		self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_index'), post_data, follow=True)
		
		users = User.objects.all()
		slps = SocialLaunchProfile.objects.all()
		
		self.assertEquals(len(users), 2)
		self.assertEquals(len(slps), 1)
		
		user = users[1]
		slp = slps[0]
		
		self.assertRedirects(response, reverse('social_launch_referral', kwargs={'referring_user_id' : user.id}))
		
		self.assertEquals(user.email, post_data['email'])
		self.assertEquals(user.username, post_data['email'])
		self.assertFalse(user.has_usable_password())
		self.assertContains(response, user_successfully_created_msg)
		self.assertEquals(slp.user, user)
		self.assertEquals(slp.referrer_url, referrer_url)
		self.assertEquals(slp.referring_user, None)
		
	def test_post_fails_invalid_email(self):
		post_data = {'email' : 'fooexample.com'}
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_index'), post_data)
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, user_successfully_created_msg)
		
	def test_post_fails_invalid_email_with_referrer(self):
		referrer_url = 'http://facebook.com'
		
		post_data = {'email' : 'fooexample.com'}
		
		session = SessionStore()
		session[referrer_url_session_key] = referrer_url
		session[referring_user_id_session_key] = ''
		session.save()
		self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_index'), post_data)
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, user_successfully_created_msg)
		self.assertEqual(self.client.session[referrer_url_session_key], referrer_url)
		
	def test_post_fails_no_email(self):
		post_data = {}
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_index'), post_data)
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, user_successfully_created_msg)
		
class ReferralTestCase(BaseTestCase):
	def test_get_success(self):
		response = self.client.get(reverse('social_launch_referral', kwargs={'referring_user_id' : self.user1.id}))
		self.assertEqual(response.status_code, 200)
		
	def test_get_fails_invalid_id(self):
		response = self.client.get(reverse('social_launch_referral', kwargs={'referring_user_id' : 'foo'}))
		
		self.assertEqual(response.status_code, 404)
		
	def test_get_fails_no_such_user(self):
		response = self.client.get(reverse('social_launch_referral', kwargs={'referring_user_id' : 1000}))
		
		self.assertEqual(response.status_code, 404)
		
	def test_post_success_creates_new_user(self):
		post_data = {'email' : 'foo@example.com'}
		
		session = SessionStore()
		session[referring_user_id_session_key] = self.user1.id
		session.save()
		self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_referral', kwargs={'referring_user_id' : self.user1.id}), post_data, follow=True)
		
		users = User.objects.all()
		slps = SocialLaunchProfile.objects.all()
		
		self.assertEquals(len(users), 2)
		self.assertEquals(len(slps), 1)
		
		user = users[1]
		slp = slps[0]
		
		self.assertRedirects(response, reverse('social_launch_referral', kwargs={'referring_user_id' : user.id}))
		
		self.assertEquals(user.email, post_data['email'])
		self.assertEquals(user.username, post_data['email'])
		self.assertFalse(user.has_usable_password())
		self.assertContains(response, user_successfully_created_msg)
		self.assertEquals(slp.user, user)
		self.assertEquals(slp.referrer_url, '')
		self.assertEquals(slp.referring_user, self.user1)
		
	def test_post_success_creates_new_user_bad_referring_used_id(self):
		post_data = {'email' : 'foo@example.com'}
		
		session = SessionStore()
		session[referring_user_id_session_key] = 1000
		session.save()
		self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
		
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(SocialLaunchProfile.objects.count(), 0)
		
		response = self.client.post(reverse('social_launch_referral', kwargs={'referring_user_id' : self.user1.id}), post_data, follow=True)
		
		users = User.objects.all()
		slps = SocialLaunchProfile.objects.all()
		
		self.assertEquals(len(users), 2)
		self.assertEquals(len(slps), 1)
		
		user = users[1]
		slp = slps[0]
		
		self.assertRedirects(response, reverse('social_launch_referral', kwargs={'referring_user_id' : user.id}))
		
		self.assertEquals(user.email, post_data['email'])
		self.assertEquals(user.username, post_data['email'])
		self.assertFalse(user.has_usable_password())
		self.assertContains(response, user_successfully_created_msg)
		self.assertEquals(slp.user, user)
		self.assertEquals(slp.referrer_url, '')
		self.assertEquals(slp.referring_user, None)
		
