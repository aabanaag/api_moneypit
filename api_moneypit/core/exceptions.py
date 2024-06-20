from rest_framework.serializers import ValidationError


class InvalidFileTypeError(ValidationError):
    def __init__(self, message="Invalid file type. Only CSV files are allowed."):
        super().__init__(message)


class InvalidCSVFileError(ValidationError):
    def __init__(self, message="Invalid CSV file."):
        super().__init__(message)


class InvalidCSVFileColumnsError(ValidationError):
    def __init__(
        self,
        message="CSV file must contain columns: symbol, qty, price, type.",
    ):
        super().__init__(message)


class InvalidCSVFileMissingValuesError(ValidationError):
    def __init__(self, message="CSV file contains missing values."):
        super().__init__(message)
