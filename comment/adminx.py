from django.contrib import admin
from .models import Comment
import xadmin
from mysite_3.base_admin import BaseOwnerAdmin
# Register your models here.


@xadmin.sites.register(Comment)
# @admin.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
	list_display = ('target', 'nickname', 'email', 'content', 'website', 'created_time')

