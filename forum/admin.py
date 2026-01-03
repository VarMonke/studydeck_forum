from django.contrib import admin
from .models import Category, Tag, Thread, Reply, Resource

admin.site.register(Thread)
admin.site.register(Reply)
admin.site.register(Resource)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
