from dataclasses import dataclass
from enum import Enum


class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"


@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency = Currency.EUR

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"
