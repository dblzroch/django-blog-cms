"""Blog views."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Comment, Post, Tag


def post_list(request, tag_slug=None, category_slug=None):
    """List published posts with optional tag/category filter."""
    posts = Post.objects.filter(status="published").order_by("-published_at")

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(
        request,
        "blog/post_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "tags": tags,
            "current_tag": tag_slug,
            "current_category": category_slug,
        },
    )


def post_detail(request, slug):
    """Show a single post with its approved comments."""
    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.comments.filter(status="approved").order_by("-created_at")  # type: ignore[attr-defined]
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments},
    )


def add_comment(request, slug):
    """Add a comment to a post."""
    post = get_object_or_404(Post, slug=slug, status="published")

    if request.method == "POST":
        author_name = request.POST.get("author_name", "").strip()
        author_email = request.POST.get("author_email", "").strip()
        content = request.POST.get("content", "").strip()

        if not author_name or not author_email or not content:
            messages.error(request, "Please fill in all fields.")
            return redirect("blog:post_detail", slug=slug)

        Comment.objects.create(
            post=post,
            author_name=author_name,
            author_email=author_email,
            content=content,
            status="pending",
        )
        messages.success(request, "Your comment is pending moderation.")
        return redirect("blog:post_detail", slug=slug)

    return redirect("blog:post_detail", slug=slug)
