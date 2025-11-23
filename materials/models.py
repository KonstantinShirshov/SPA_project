from django.db import models


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
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
