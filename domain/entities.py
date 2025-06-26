from dataclasses import dataclass
from .value_objects import Money


auto_increment_id = {
    'client': 0,
    'room': 0,
    'reservation': 0
}

def _next_id(entity: str) -> int:
    auto_increment_id[entity] += 1
    return auto_increment_id[entity]


@dataclass
class Client:
    full_name: str
    email: str
    phone: str
    id: int = None

    def __post_init__(self):
        if self.id is None:
            self.id = _next_id('client')


@dataclass
class Room:
    room_type: str
    price_per_night: Money
    id: int = None

    def __post_init__(self):
        if self.id is None:
            self.id = _next_id('room')


@dataclass
class Reservation:
    client_id: int
    room_id: int
    check_in: str
    nights: int
    total_amount: Money
    confirmed: bool = False
    id: int = None

    def __post_init__(self):
        if self.id is None:
            self.id = _next_id('reservation')
