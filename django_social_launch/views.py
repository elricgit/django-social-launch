#Django imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

#App imports
from . import referrer_url_session_key, referring_user_id_session_key, user_successfully_created_msg
from forms import UserSignupForm
from models import SocialLaunchProfile
from registration.backends.default import DefaultBackend

def index(request, referring_user_id=None):
	referring_user = None
	has_registered = False
	referrer_count = None
	
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = DefaultBackend().register(
				request,
				password1 = None,
				email = email,
				username = email,
			)
			
			request.session['username'] = user.username
			
			SocialLaunchProfile.objects.create_from_request(user, request)
			
			messages.success(request, user_successfully_created_msg)
			return redirect('social_launch_referral', referring_user_id=user.id)
	else:
		form = UserSignupForm()
		form.fields['referrer_url'].initial = request.META.get('HTTP_REFERER', '')
		if referring_user_id is not None:
			try:
				referring_user = get_object_or_404(User, id=referring_user_id)
			except ValueError:
				raise Http404
		
		has_registered = request.user.is_authenticated() or request.session.get('username', '')
		
		if has_registered:
			referrer_count = SocialLaunchProfile.objects.filter(referring_user=referring_user).count()
			form = None
		else:
			form = UserSignupForm()
			
			if referrer_url_session_key not in request.session:
				request.session[referrer_url_session_key] = request.META.get('HTTP_REFERER', '')
			if referring_user_id_session_key not in request.session:
				request.session[referring_user_id_session_key] = referring_user_id if referring_user_id is not None else ''
		
	return render(request, 'social_launch/index.html', {'form' : form, 'has_registered' : has_registered, 'referrer_count' : referrer_count})

