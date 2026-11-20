"""Tests for django-blog-cms blog app."""

import pytest
from blog.models import Category, Comment, Post, Tag
from django.contrib.auth.models import User
from django.urls import reverse


# ------------------------------------------------------------------
# Models: Category
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_category_str():
    cat = Category.objects.create(name="Tech", slug="tech")
    assert str(cat) == "Tech"


# ------------------------------------------------------------------
# Models: Tag
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_tag_str():
    tag = Tag.objects.create(name="Python", slug="python")
    assert str(tag) == "Python"


# ------------------------------------------------------------------
# Models: Post
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_post_str_and_url():
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    post = Post.objects.create(
        title="My First Post",
        slug="my-first-post",
        content="# Hello\n\nThis is **markdown**.",
        category=cat,
        author=user,
        status="published",
    )
    assert str(post) == "My First Post"
    assert post.get_absolute_url() == "/my-first-post/"
    assert (
        post.content_as_markdown()
        == "<h1>Hello</h1>\n<p>This is <strong>markdown</strong>.</p>"
    )


# ------------------------------------------------------------------
# Models: Comment
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_comment_str():
    Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    post = Post.objects.create(
        title="Post", slug="post", content="content", author=user, status="published"
    )
    comment = Comment.objects.create(
        post=post,
        author_name="Reader",
        author_email="reader@example.com",
        content="Nice post!",
    )
    assert str(comment) == "Comment by Reader on Post"


# ------------------------------------------------------------------
# Views: post_list
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_post_list_view(client):
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    Post.objects.create(
        title="Published Post",
        slug="published-post",
        content="content",
        category=cat,
        author=user,
        status="published",
    )
    Post.objects.create(
        title="Draft Post",
        slug="draft-post",
        content="content",
        category=cat,
        author=user,
        status="draft",
    )
    url = reverse("blog:post_list")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Published Post" in response.content
    assert b"Draft Post" not in response.content


# ------------------------------------------------------------------
# Views: post_detail
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_post_detail_view(client):
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    post = Post.objects.create(
        title="Detail Post",
        slug="detail-post",
        content="content",
        category=cat,
        author=user,
        status="published",
    )
    url = reverse("blog:post_detail", args=[post.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert b"Detail Post" in response.content


# ------------------------------------------------------------------
# Views: post_list filtered by tag
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_post_list_by_tag(client):
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    tag = Tag.objects.create(name="Django", slug="django")
    post = Post.objects.create(
        title="Django Post",
        slug="django-post",
        content="content",
        category=cat,
        author=user,
        status="published",
    )
    post.tags.add(tag)

    url = reverse("blog:post_list_by_tag", args=["django"])
    response = client.get(url)
    assert response.status_code == 200
    assert b"Django Post" in response.content


# ------------------------------------------------------------------
# Views: add_comment
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_add_comment(client):
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    post = Post.objects.create(
        title="Commentable",
        slug="commentable",
        content="content",
        category=cat,
        author=user,
        status="published",
    )

    url = reverse("blog:add_comment", args=[post.slug])
    response = client.post(
        url,
        {
            "author_name": "Reader",
            "author_email": "reader@example.com",
            "content": "Great post!",
        },
    )
    assert response.status_code == 302

    comment = Comment.objects.get(post=post)
    assert comment.status == "pending"
    assert comment.author_name == "Reader"


# ------------------------------------------------------------------
# Views: post_list filtered by category
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_post_list_by_category(client):
    cat1 = Category.objects.create(name="Dev", slug="dev")
    cat2 = Category.objects.create(name="Design", slug="design")
    user = User.objects.create_user(username="author", password="pass123")
    Post.objects.create(
        title="Dev Post",
        slug="dev-post",
        content="content",
        category=cat1,
        author=user,
        status="published",
    )
    Post.objects.create(
        title="Design Post",
        slug="design-post",
        content="content",
        category=cat2,
        author=user,
        status="published",
    )

    url = reverse("blog:post_list_by_category", args=["design"])
    response = client.get(url)
    assert response.status_code == 200
    assert b"Design Post" in response.content
    assert b"Dev Post" not in response.content


# ------------------------------------------------------------------
# Sitemap
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_sitemap_includes_published_posts():
    cat = Category.objects.create(name="Dev", slug="dev")
    user = User.objects.create_user(username="author", password="pass123")
    Post.objects.create(
        title="Sitemap Post",
        slug="sitemap-post",
        content="content",
        category=cat,
        author=user,
        status="published",
    )
    Post.objects.create(
        title="Draft Post",
        slug="draft-post",
        content="content",
        category=cat,
        author=user,
        status="draft",
    )

    from blog.sitemaps import PostSitemap

    sitemap = PostSitemap()
    items = list(sitemap.items())
    assert len(items) == 1
    assert items[0].title == "Sitemap Post"
    assert items[0].slug == "sitemap-post"


# ------------------------------------------------------------------
# CLI / management
# ------------------------------------------------------------------
def test_manage_py_exists():
    import os

    assert os.path.exists("manage.py")
