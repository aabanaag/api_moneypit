import pandas as pd
from rest_framework import serializers

from api_moneypit.core.exceptions import InvalidCSVFileColumns
from api_moneypit.core.exceptions import InvalidCSVFileError
from api_moneypit.core.exceptions import InvalidCSVFileMissingValues
from api_moneypit.core.exceptions import InvalidFileTypeError
from api_moneypit.core.models import BulkOrder
from api_moneypit.core.models import Order
from api_moneypit.core.models import Ticker
from api_moneypit.users.api.serializers import UserSerializer


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = "__all__"


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "ticker", "qty", "price", "type", "user", "status")
        extra_kwargs = {
            "user": {"required": False},
            "id": {"read_only": True},
        }


class OrderRetrieveSerializer(serializers.ModelSerializer):
    ticker = TickerSerializer()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class BulkOrderSerializer(serializers.ModelSerializer):
    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise InvalidFileTypeError

        try:
            csv_dataframe = pd.read_csv(value)
        except pd.errors.ParserError as err:
            raise InvalidCSVFileError from err

        required_columns = ["symbol", "qty", "price", "type"]
        if not all(column in csv_dataframe.columns for column in required_columns):
            raise InvalidCSVFileColumns

        if csv_dataframe.isna().to_numpy().any():
            raise InvalidCSVFileMissingValues

        return value

    class Meta:
        model = BulkOrder
        fields = ("id", "file", "user", "is_processed")
        extra_kwargs = {
            "user": {"required": False},
            "id": {"read_only": True},
            "is_processed": {"read_only": True},
        }
