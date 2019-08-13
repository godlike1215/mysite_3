from django.contrib import admin


class BaseOwnerAdmin:
	exclude = ('owner',)

	def get_list_queryset(self):
		request = self.request
		qs = super().get_list_queryset()
		return qs.filter(owner=request.user)

	def save_models(self):
		self.new_obj.owner = self.request.user
		return super().save_models()

# class BaseOwnerAdmin(admin.ModelAdmin):
# 	exclude = ('owner',)
#
# 	def get_queryset(self, request):
# 		qs = super().get_queryset(request)
# 		return qs.filter(owner=request.user)
#
# 	def save_model(self, request, obj, form, change):
# 		obj.owner = request.user
# 		return super().save_model(request, obj, form, change)
