from django.contrib import admin

from .models import Category, Location, Post, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'text',
        'author',
        'category',
        'location',
        'pub_date'
    )
    list_editable = (
        'is_published',
        'category',
        'location'
    )
    list_display_links = ('title',)
    list_filter = ('is_published',)


admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Post, PostAdmin)
