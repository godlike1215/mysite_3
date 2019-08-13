import xadmin
from mysite_3.base_admin import BaseOwnerAdmin
from django.contrib import admin
from.models import Link, SideBar

# Register your models here.


@xadmin.sites.register(Link)
# @admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
	list_display = ('title', 'href', 'status', 'weight', 'created_time')
	fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(SideBar)
# @admin.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
	list_display = ('title', 'display_type', 'content', 'created_time')
	fields = ('title', 'status', 'display_type', 'content')
