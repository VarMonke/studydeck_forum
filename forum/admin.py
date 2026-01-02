from django.contrib import admin
from .models import Category, Tag, Thread, Reply

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Thread)
admin.site.register(Reply)