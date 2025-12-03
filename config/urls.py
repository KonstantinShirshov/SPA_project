from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("materials.urls", namespace="courses")),
    path("payments/", include("users.urls", namespace="payments")),
]
