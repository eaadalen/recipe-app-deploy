from django.urls import path
from .views import home, records, about_me, RecipeListView, RecipeDetailView

app_name = "recipes"

urlpatterns = [
    path("", home),
    path("records", records),
    path("about_me", about_me),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail")
]