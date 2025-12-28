from django.db import models

from materials.validators import validate_youtube_url
from users.models import User


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
        blank="True",
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="courses",
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        validators=[validate_youtube_url],
        help_text="Укажите ссылку на видео",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="lessons",
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} - {self.course}"
