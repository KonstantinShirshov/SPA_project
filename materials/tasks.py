from datetime import timedelta

from black import timezone

from materials.models import Course, Subscription
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task
def info_email(course_id):
    course = Course.objects.get(pk=course_id)
    now = timezone.now()
    if now - course.updated_at < timedelta(minutes=1):
        return
    subscribers = Subscription.objects.filter(course_id=course_id)
    for subscriber in subscribers:
        send_mail(
            subject="Оповещение",
            message=f"Курс {course.name} обновлён",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.user.email],
            fail_silently=True
        )
