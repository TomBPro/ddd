from dataclasses import dataclass
from enum import Enum

RATES_TO_EUR = {
    'EUR': 1.0,
    'USD': 0.9,
    'GBP': 1.15,
    'JPY': 0.007,
    'CHF': 1.0,
}


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

    def convert_to(self, target: Currency) -> 'Money':
        """Return a new Money value converted to another currency."""
        if self.currency == target:
            return Money(self.amount, self.currency)
        rate_from = RATES_TO_EUR[self.currency.value]
        amount_in_eur = self.amount * rate_from
        if target == Currency.EUR:
            return Money(amount_in_eur, Currency.EUR)
        rate_to = RATES_TO_EUR[target.value]
        converted = amount_in_eur / rate_to
        return Money(converted, target)
