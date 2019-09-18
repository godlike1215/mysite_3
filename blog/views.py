from datetime import date
from django.db.models import Q, F
from django.shortcuts import render
from django.template.loader import render_to_string


from .models import Post, Tag, Category
from config.models import SideBar, Link
from comment.models import Comment
from django.views.generic import ListView, DetailView
from comment.forms import CommentForm
from django.core.cache import cache

# Create your views here.


# def post_list(request, category_id=None, tag_id=None):
# 	category = None
# 	tag = None
#
# 	if tag_id:
# 		post_list, tag = Post.get_by_tag(tag_id)
# 	elif category_id:
# 		post_list, category = Post.get_by_category(category_id)
# 	else:
# 		post_list = Post.latest_posts()
#
# 	context = {
# 		'category': category,
# 		'tag': tag,
# 		'post_list': post_list,
# 		'sidebars': SideBar.get_sidebars()
# 	}
# 	context.update(Category.get_navs())
# 	return render(request, 'index.html', context)


class CommonViewMixin:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'sidebars': SideBar.get_sidebars(),
		})
		context.update(Category.get_navs())
		return context


class IndexView(CommonViewMixin, ListView):
	queryset = Post.latest_posts()
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 5


class CategoryView(IndexView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category_id = self.kwargs.get('category_id')
		context.update({
			'category': Category.objects.filter(id=category_id)
		})
		return context

	def get_queryset(self):
		queryset = super().get_queryset()
		category_id = self.kwargs.get('category_id')
		return queryset.filter(category_id=category_id)


# def post_detail(request, post_id=None):
# 	try:
# 		post = Post.objects.get(id=post_id)
# 	except Post.DoesNotExist:
# 		post = None
# 	context = {
# 		'post': post,
# 		'sidebars': SideBar.get_sidebars()
# 	}
# 	context.update(Category.get_navs())
# 	return render(request, 'post.html', {'post': post})


class PostDetailView(CommonViewMixin, DetailView):
	queryset = Post.latest_posts()
	template_name = 'blog/post.html'
	context_object_name = 'post'
	pk_url_kwarg = 'post_id'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'comment_form': CommentForm,
			'comment_list': Comment.get_by_target(self.request.path)
		})
		return context

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		# print(response)
		# 得到一个Post对象
		# print(type(self.object))
		# 获取queryset对象
		# post_obj = Post.objects.get(pk=self.object.id)
		# post_obj.pv = F('pv') + 1
		# post_obj.save()
		# 上面三行是麻烦的写法，下面的是简便写法,用update方法
		# Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
		self.handle_visited()
		return response

	def handle_visited(self):
		increase_pv = False
		increase_uv = False
		uid = self.request.uid
		print(uid)
		pv_key = 'pv:%s:%s' % (uid, self.request.path)
		uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
		if not cache.get(pv_key):
			increase_pv = True
			cache.set(pv_key, 1, 1*60)  # 1分钟有效

		if not cache.get(uv_key):
			increase_uv = True
			cache.set(pv_key, 1, 24*60*60)   # 24小时有效

		if increase_uv and increase_pv:
			Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)

		elif increase_pv:
			Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
		elif increase_uv:
			Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)


class SearchView(IndexView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		keyword = self.request.GET.get('keyword1', '')
		context.update({'keyword': keyword})
		return context

	def get_queryset(self):
		queryset = super().get_queryset()
		keyword = self.request.GET.get('keyword1', '')
		if not keyword:
			return queryset
		return queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))


class AuthorView(IndexView):
	def get_queryset(self):
		qs = super().get_queryset()
		author_id = self.kwargs.get('author_id')
		return qs.filter(owner_id=author_id)

