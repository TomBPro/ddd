from abc import ABC, abstractmethod
from .entities import Client, Room, Reservation, Payment


class ClientRepository(ABC):
    @abstractmethod
    def add(self, client: Client) -> None:
        ...

    @abstractmethod
    def get(self, client_id: int) -> Client | None:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Client | None:
        ...

    @abstractmethod
    def save(self, client: Client) -> None:
        ...


class RoomRepository(ABC):
    @abstractmethod
    def add(self, room: Room) -> None:
        ...

    @abstractmethod
    def get(self, room_id: int) -> Room | None:
        ...

    @abstractmethod
    def list(self) -> list[Room]:
        ...


class ReservationRepository(ABC):
    @abstractmethod
    def add(self, reservation: Reservation) -> None:
        ...

    @abstractmethod
    def get(self, reservation_id: int) -> Reservation | None:
        ...

    @abstractmethod
    def list(self) -> list[Reservation]:
        ...

    @abstractmethod
    def remove(self, reservation_id: int) -> None:
        ...

    @abstractmethod
    def save(self, reservation: Reservation) -> None:
        ...


class PaymentRepository(ABC):
    @abstractmethod
    def add(self, payment: Payment) -> None:
        ...

    @abstractmethod
    def list_for_client(self, client_id: int) -> list[Payment]:
        ...
