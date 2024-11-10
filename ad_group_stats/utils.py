import decimal
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek

COMPARE_MODE = ['preceding', 'previous_month']
AGGREGATE_BY = ['day', 'week', 'month']


def aggregate_map(aggregate):
    AGGREGATE_MAP = {
        'day': TruncDate('date'),
        'week': TruncWeek('date'),
        'month': TruncMonth('date'),
    }
    return AGGREGATE_MAP.get(aggregate)


def get_previouse_dates(start_date, end_date, compare_mode):
    if compare_mode == "preceding":
        days_delta = (end_date - start_date).days + 1
        previous_start_date = start_date - timedelta(days=days_delta)
        previous_end_date = end_date - timedelta(days=days_delta)
    elif compare_mode == "previous_month":
        previous_start_date = start_date - relativedelta(months=1)
        previous_end_date = end_date - relativedelta(months=1)

    return previous_start_date, previous_end_date


def quantize_two_decimal_places(amount):
    return decimal.Decimal(amount).quantize(
        decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP
    )
