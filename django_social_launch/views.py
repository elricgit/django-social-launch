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

def index(request, referring_user_id=None):
	referring_user = None
	if referring_user_id is not None:
		try:
			referring_user = get_object_or_404(User, id=referring_user_id)
		except ValueError:
			raise Http404
	
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.email
			user.save()
			
			slp = SocialLaunchProfile(user=user, referrer_url=form.cleaned_data['referrer_url'], referring_user=referring_user)
			slp.save()
			
			messages.success(request, user_successfully_created_msg)
			return redirect('social_launch_referral', referring_user_id=user.id)
	else:
		form = UserSignupForm()
		form.fields['referrer_url'].initial = request.META.get('HTTP_REFERER', '')
		
	return render(request, 'social_launch/index.html', {'form' : form,})
	

