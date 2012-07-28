#Django imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

#App imports
from forms import UserSignupForm
from models import SocialLaunchProfile

# Create your views here.

user_successfully_created_msg = 'You successfully edited your profile.'

referrer_url_session_key = 'social_launch_referrer_url'
referring_user_id_session_key = 'social_launch_referring_user_id'

def index(request, referring_user_id=None):
	referring_user = None
		
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.email
			user.save()
			
<<<<<<< HEAD
			slp = SocialLaunchProfile(user=user, referrer_url=form.cleaned_data['referrer_url'], referring_user=referring_user)
=======
			referrer_url = request.session.get(referrer_url_session_key, '')
			
			referring_user_id = request.session.get(referring_user_id_session_key, None)
			
			if referring_user_id:
				try:
					referring_user = get_object_or_404(User, id=referring_user_id)
				except ValueError:
					pass
			
			slp = SocialLaunchProfile(
				user=user,
				referrer_url=referrer_url,
				referring_user=referring_user,
			)
>>>>>>> b78e863fc11a8645ff4a499a5876b1b1685f37fe
			slp.save()
			
			messages.success(request, user_successfully_created_msg)
			return redirect('social_launch_referral', referring_user_id=user.id)
	else:
<<<<<<< HEAD
		form = UserSignupForm()
		form.fields['referrer_url'].initial = request.META.get('HTTP_REFERER', '')
=======
		if referring_user_id is not None:
			try:
				referring_user = get_object_or_404(User, id=referring_user_id)
			except ValueError:
				raise Http404
		
		if request.user.is_authenticated():
			#TESTME
			form = None
		else:
			form = UserSignupForm()
			request.session[referrer_url_session_key] = request.META.get('HTTP_REFERER', '')
			request.session[referring_user_id_session_key] = referring_user_id if referring_user_id is not None else ''
>>>>>>> b78e863fc11a8645ff4a499a5876b1b1685f37fe
		
	return render(request, 'social_launch/index.html', {'form' : form,})

