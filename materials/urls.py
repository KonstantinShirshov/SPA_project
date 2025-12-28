from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionAPIView,
)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("subscription/", SubscriptionAPIView.as_view(), name="subscribe"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons-delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons-update"
    ),
]

urlpatterns += router.urls
