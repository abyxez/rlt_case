from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Row:
    price: int
    date: datetime


@dataclass
class Data:
    rows: list[Row]


class Aggregator:
    def __init__(self, by="month"):
        self.by = by

    def adjust_date_to_period_start(self, date: datetime) -> datetime:
        if self.by == "year":
            return datetime(date.year, 0, 0, 0)
        elif self.by == "month":
            return datetime(date.year, date.month, 1, 0)
        elif self.by == "day":
            return datetime(date.year, date.month, date.day, 0)
        elif self.by == "hour":
            return datetime(date.year, date.month, date.day, date.hour)
        else:
            raise ValueError(f"Unsupported aggregation period: {self.by}")

    def aggregate(self, data: Data) -> Data:
        grouped_data = defaultdict(int)
        for row in data.rows:
            adjusted_date = self.adjust_date_to_period_start(row.date)
            grouped_data[adjusted_date] += row.price

        aggregated_rows = [
            Row(price=price, date=date) for date, price in grouped_data.items()
        ]

        return Data(aggregated_rows)
