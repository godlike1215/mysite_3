from django.contrib import admin
from .models import Comment
from mysite_3.base_admin import BaseOwnerAdmin
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('target', 'nickname', 'email', 'content', 'website', 'created_time')

