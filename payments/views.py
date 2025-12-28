from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, viewsets
from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["course", "lesson", "pay_method"]
    search_fields = ["user__email", "course__name"]
    ordering_fields = ["paid_at"]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course is None and payment.lesson is None:
            raise ValidationError("Нужно выбрать курс или урок")
        elif payment.course and payment.lesson:
            raise ValidationError("Нужно выбрать либо курс, либо урок")
        else:
            if payment.course:
                product = create_stripe_product(payment.course)
            else:
                product = create_stripe_product(payment.lesson)
        price = create_stripe_price(stripe_product=product, amount=payment.amount)
        session_id, session_url =create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()
