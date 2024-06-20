from django.db.models import DecimalField
from django.db.models import F
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_moneypit.core.api.filters import OrderFilter
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
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_class = OrderFilter
    search_fields = ["ticker__symbol", "ticker__name"]

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
    def bulk_order(self, request):
        serializer = BulkOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="total_order")
    def total_order(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        filterset = self.filter_class(request.query_params, queryset=queryset)
        filtered_queryset = filterset.qs

        total_order_query = filtered_queryset.aggregate(
            total_orders=Coalesce(
                Sum(F("qty") * F("price")), 0, output_field=DecimalField()
            )
        )
        total_order = total_order_query.get("total_orders", 0)

        return Response(
            {
                "total_order": total_order,
                "symbol": request.query_params.get("symbol", None),
            },
            status=status.HTTP_200_OK,
        )
