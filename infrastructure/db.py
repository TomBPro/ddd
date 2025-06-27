from domain.services import ReservationService
from .repositories import (
    init_schema as _init_schema,
    DB_PATH as _DB_PATH,
    JsonClientRepository,
    JsonRoomRepository,
    JsonReservationRepository,
    JsonPaymentRepository,
)

DB_PATH = _DB_PATH


def init_schema() -> None:
    _init_schema()

_service: ReservationService | None = None


def _get_service() -> ReservationService:
    global _service
    if _service is None:
        init_schema()
        _service = ReservationService(
            JsonClientRepository(),
            JsonRoomRepository(),
            JsonReservationRepository(),
            JsonPaymentRepository(),
        )
    return _service


def add_client(full_name: str, email: str, phone: str) -> int:
    return _get_service().add_client(full_name, email, phone).id


def deposit(client_id: int, amount: float, currency: str = "EUR") -> float:
    return _get_service().deposit(client_id, amount, currency)


def add_room(room_type: str, price: float, description: str) -> int:
    return _get_service().add_room(room_type, price, description).id


def list_rooms() -> list:
    rooms = _get_service().list_rooms()
    return [
        {
            "id": r.id,
            "room_type": r.room_type,
            "price": r.price_per_night.amount,
            "description": r.description,
        }
        for r in rooms
    ]


def add_reservation(client_id: int, room_id: int, check_in: str, nights: int) -> int:
    return _get_service().add_reservation(client_id, room_id, check_in, nights).id


def confirm_reservation(reservation_id: int) -> None:
    _get_service().confirm_reservation(reservation_id)


def cancel_reservation(reservation_id: int) -> None:
    _get_service().cancel_reservation(reservation_id)
