from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UserForm(ModelForm):
	password = forms.CharField(label='密码', widget=forms.PasswordInput)
	password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

	def clean_password2(self):
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if password != password2:
			raise forms.ValidationError('密码错误')
		return password2

	class Meta:
		model = User
		fields = ['username', 'email']

