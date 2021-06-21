from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewUserForm2(NewUserForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField()

	class Meta:
		model = User
		fields = ("username", "email","first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm2, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.lastt_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user
