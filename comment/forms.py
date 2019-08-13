from django import forms
from comment.models import Comment
import mistune


class CommentForm(forms.ModelForm):
	# 先这么写吧，用CharField，具体去查文档
	nickname = forms.CharField(
		label='昵称',
		max_length=50,
		widget=forms.widgets.Input(
			attrs={'class': 'form-control', 'style': 'width: 60%;'}
		)
	)
	email = forms.CharField(
		label='Email',
		max_length=50,
		widget=forms.widgets.EmailInput(
			attrs={'class': 'form-control', 'style': 'width: 60%'}
		)
	)
	website = forms.CharField(
		label='网站',
		max_length=100,
		widget=forms.URLInput(
			attrs={'class': 'form-control', 'style': 'width: 60%'}
		)
	)
	content = forms.CharField(
		label='内容',
		max_length=500,
		widget=forms.widgets.Textarea(
			attrs={'row': 6, 'cols': 60, 'class': 'form-control'}
		)
	)

	class Meta:
		model = Comment
		fields = ['nickname', 'email', 'website', 'content']

	def clean_content(self):
		# self.clean_data得到的是一个字典，其中存储了上面几个字段的信息
		content = self.cleaned_data.get('content')
		# print(content)
		content = mistune.markdown(content)
		# print(content)
		if len(content) < 10:
			raise forms.ValidationError('太短了！要大于10')
		return content
