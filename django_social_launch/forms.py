#Django imports
from django import forms
from django.contrib.auth.models import User

# place form definitions here
class UserSignupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserSignupForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		
	def clean(self):
		cleaned_data = self.cleaned_data
		
		self.instance.set_unusable_password()
		
		return cleaned_data
	
	class Meta:
		model = User
		fields = ('email',)
