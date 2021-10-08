from django.contrib import admin

from .models import Post, PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "status")


admin.site.register(PostImage)
admin.site.register(Post, PostAdmin)
