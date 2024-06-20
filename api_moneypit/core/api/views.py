from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_moneypit.core.api.serializers import BulkOrderSerializer
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

    @action(detail=False, methods=["post"], url_path="bulk_order")
    def bulk_order(self, request, pk=None):
        serializer = BulkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
