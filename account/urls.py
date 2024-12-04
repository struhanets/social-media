from django.urls import path, include
from rest_framework import routers

from account import views

router = routers.DefaultRouter()

router.register("profiles", views.ProfileViewSet)
router.register("posts", views.PostViewSet)
router.register("comments", views.CommentViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "account"
