from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api_moneypit.core.models import Order

from api_moneypit.core.api.serializers import (
    OrderListSerializer,
    OrderRetrieveSerializer,
    OrderCreateUpdateSerializer
)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return OrderRetrieveSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderListSerializer

