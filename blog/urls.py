"""Blog URLs."""

from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "category/<slug:category_slug>/", views.post_list, name="post_list_by_category"
    ),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("<slug:slug>/comment/", views.add_comment, name="add_comment"),
]
