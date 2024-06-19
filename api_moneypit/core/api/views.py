from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api_moneypit.core.api.serializers import OrderCreateUpdateSerializer
from api_moneypit.core.api.serializers import OrderListSerializer
from api_moneypit.core.api.serializers import OrderRetrieveSerializer
from api_moneypit.core.models import Order
from api_moneypit.core.permissions import IsOwnerOrReadOnly


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return OrderCreateUpdateSerializer
        else:
            return OrderListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
