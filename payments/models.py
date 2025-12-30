from django.db import models

from materials.models import Course, Lesson
from users.models import User


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("bank", "Перевод на счёт"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    paid_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма", null=True, blank=True)
    pay_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, blank=True, null=True
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите Id сессии",
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        studying_product = self.course or self.lesson
        return f"{self.user} оплатил {studying_product} на сумму {self.amount}₽"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
