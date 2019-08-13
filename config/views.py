from django.shortcuts import render
from blog.views import CommonViewMixin
from .models import Link
from django.views.generic import ListView

# Create your views here.


class LinkListView(CommonViewMixin, ListView):
	queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
	# model = Link
	template_name = 'config/links.html'
	context_object_name = 'link_list'
