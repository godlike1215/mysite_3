from dal import autocomplete
from django import forms
from blog.models import Category, Tag, Post
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
	description = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
	category = forms.ModelChoiceField(
		queryset=Category.objects.all(),
		widget=autocomplete.ModelSelect2(url='category-autocomplete'),
		label='分类',
	)
	tags = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
		label='标签',
	)

	content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
	content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
	content = forms.CharField(widget=forms.HiddenInput(), label='正文', required=False)

	class Meta:
		model = Post
		fields = ('category', 'tags', 'description', 'title',
				  'is_md', 'content', 'content_md', 'content_ck',
				  'status')

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial') or {}
		instance = kwargs.get('instance')
		if instance:
			if instance.is_md:
				initial['content_md'] = instance.content
			else:
				initial['content_ck'] = instance.content
		kwargs.update({'initial': initial})
		super().__init__(*args, **kwargs)

	def clean(self):
		is_md = self.cleaned_data.get('is_md')
		if is_md:
			content_field_name = 'content_md'
		else:
			content_field_name = 'content_ck'
		content = self.cleaned_data.get(content_field_name)
		print(content)
		if not content:
			self.add_error(content_field_name, '必须填！')
			return
		self.cleaned_data['content'] = content
		return super().clean()

