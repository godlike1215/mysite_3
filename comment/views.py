from django.shortcuts import render
from django.shortcuts import redirect
from .forms import CommentForm
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate

# Create your views here.


class CommentView(TemplateView):
	# 默认接受全部请求方法，改为只接受post请求
	http_method_names = ['post']
	template_name = 'comment/result.html'

	def post(self, request, *args, **kwargs):
		comment_form = CommentForm(request.POST)
		target = request.POST.get('target')

		if comment_form.is_valid():
			instance = comment_form.save(commit=False)
			instance.target = target
			instance.save()
			succeed = True
			return redirect(target)
		else:
			succeed = False

		context = {
			'succeed': succeed,
			'form': comment_form,
			'target': target
		}
		# 显示forms.py中clean_content中提出的异常
		# print(comment_form.errors.items())
		return self.render_to_response(context)


