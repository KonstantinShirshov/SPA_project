from rest_framework.routers import SimpleRouter

from payments.apps import PaymentsConfig
from payments.views import PaymentViewSet

app_name = PaymentsConfig.name

router = SimpleRouter()
router.register("", PaymentViewSet, basename="payment")

urlpatterns = []

urlpatterns += router.urls
