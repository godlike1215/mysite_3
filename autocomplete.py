from dal import autocomplete
from django import forms
from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Category.objects.none()

		qs = Category.objects.filter(owner=self.request.user)

		if self.q:
			print(self.q)
			qs = qs.filter(name__istartswith=self.q)
			print(qs)
		return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Category.objects.none()

		qs = Tag.objects.filter(owner=self.request.user)

		if self.q:
			qs = qs.filter(name__istartswith=self.q)
		return qs


