from django.utils import timezone
from dateutil.relativedelta import relativedelta
from celery import shared_task

from users.models import User

@shared_task
def disactive_users():
    month_ago = timezone.now() - relativedelta(months=1)
    qs= User.objects.filter(last_login__lt=month_ago, is_active=True)
    qs.update(is_active=False)

