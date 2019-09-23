from django.contrib import admin

from blog.adminforms import PostAdminForm
from .models import Category, Post, Tag
from mysite_3.base_admin import BaseOwnerAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
	list_display = ('name', 'created_time', 'owner', 'post_count')
	fields = ('name', 'status', 'is_nav')

	def post_count(self, obj):
		return obj.post_set.count()

	post_count.short_description = '文章数量'


# 装饰器最终得到的就是下面这行代码
# admin.site.register(Category, CategoryAdmin)


# class CategoryOwnerFilter(RelatedFieldListFilter):
#
# 	title = '分类过滤器'
# 	parameter_name = 'owner_category'
#
# 	def lookups(self, request, model_admin):
# 		a = Category.objects.filter(owner=request.user).values_list('id', 'name')
# 		# print(type(a))
# 		return a
#
# 	def queryset(self, request, queryset):
# 		category_id = self.value()
# 		if category_id:
# 			return queryset.filter(id=category_id)
# 		return queryset
#
# 	@classmethod
# 	def test(cls, field, request, params, model, admin_view, field_path):
# 		return field.name == 'category'
#
# 	def __init__(self, field, request, params, models, model_admin, field_path):
# 		super().__init__(field, request, params, models, model_admin, field_path)
# 		self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#
# manager.register(CategoryOwnerFilter, take_priority=True)

class CategoryOwnerFilter(admin.SimpleListFilter):

	title = '分类过滤器'
	parameter_name = 'owner_category'

	def lookups(self, request, model_admin):
		a = Category.objects.filter(owner=request.user).values_list('id', 'name')
		return a

	def queryset(self, request, queryset):
		category_id = self.value()
		if category_id:
			return queryset.filter(id=category_id)
		return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
	form = PostAdminForm
	list_display = ('title', 'category', 'owner', 'status', 'created_time')
	list_filter = (CategoryOwnerFilter,)
	search_fields = ('title',)
	fieldsets = (
		('基础信息', {
			'fields': ('title', 'category', 'tags', 'status')
		}),
		('高级', {
			'classes': ('collapse',),
			'fields': ('description', 'is_md', 'content_ck', 'content_md', 'content')
		})
	)

	save_on_top = True

	# def save_model(self, request, obj, form, change):
	# 	obj.content_html = mistune.markdown(obj.content)
	# 	# print(obj.content_html, '2')
	# 	super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name', 'owner', 'created_time')
	fields = ('name', 'status')
