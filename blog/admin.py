"""Blog admin."""

from django.contrib import admin

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at", "author")
    list_filter = ("status", "category", "tags")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author_name", "post", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("author_name", "content")
    actions = ["approve_comments", "reject_comments"]

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Reject selected comments")
    def reject_comments(self, request, queryset):
        queryset.update(status="rejected")
