from datetime import datetime, timedelta

from .entities import Client, Room, Reservation, Payment
from .value_objects import Money, Currency
from .repositories import (
    ClientRepository,
    RoomRepository,
    ReservationRepository,
    PaymentRepository,
)


class ReservationService:
    def __init__(self, client_repo: ClientRepository, room_repo: RoomRepository,
                 reservation_repo: ReservationRepository,
                 payment_repo: PaymentRepository):
        self.clients = client_repo
        self.rooms = room_repo
        self.reservations = reservation_repo
        self.payments = payment_repo

    def add_client(self, full_name: str, email: str, phone: str) -> Client:
        if self.clients.find_by_email(email) is not None:
            raise ValueError("client already exists")
        client = Client(full_name, email, phone)
        self.clients.add(client)
        return client

    def deposit(self, client_id: int, amount: float, currency: str = "EUR") -> float:
        client = self.clients.get(client_id)
        if client is None:
            raise ValueError("client not found")
        cur = currency.upper()
        if cur not in Currency.__members__:
            raise ValueError('unsupported currency')
        rate = Currency(cur)
        money = Money(amount, rate)
        client.wallet += money.convert_to(Currency.EUR).amount
        self.clients.save(client)
        self.payments.add(Payment(client_id=client.id, amount=money, kind="deposit"))
        return client.wallet

    def add_room(self, room_type: str, price: float, description: str) -> Room:
        room = Room(room_type=room_type, price_per_night=Money(price), description=description)
        self.rooms.add(room)
        return room

    def list_rooms(self) -> list[Room]:
        return self.rooms.list()

    def add_reservation(self, client_id: int, room_id: int, check_in: str, nights: int) -> Reservation:
        client = self.clients.get(client_id)
        if client is None:
            raise ValueError("client not found")
        room = self.rooms.get(room_id)
        if room is None:
            raise ValueError("room not found")
        start = datetime.fromisoformat(check_in)
        end = start + timedelta(days=nights)
        for r in self.reservations.list():
            if r.room_id != room_id:
                continue
            existing_start = datetime.fromisoformat(r.check_in)
            existing_end = existing_start + timedelta(days=r.nights)
            if start < existing_end and end > existing_start:
                raise ValueError("room not available for the selected dates")
        total = room.price_per_night.amount * nights
        if client.wallet < total / 2:
            raise ValueError("insufficient funds")
        client.wallet -= total / 2
        reservation = Reservation(client_id=client_id, room_id=room_id,
                                  check_in=check_in, nights=nights,
                                  total_amount=Money(total))
        self.reservations.add(reservation)
        self.clients.save(client)
        self.payments.add(Payment(client_id=client.id,
                                  amount=Money(total/2),
                                  kind="reservation_deposit",
                                  reservation_id=reservation.id))
        return reservation

    def confirm_reservation(self, reservation_id: int) -> None:
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            raise ValueError("reservation not found")
        if reservation.confirmed:
            return
        client = self.clients.get(reservation.client_id)
        if client is None:
            raise ValueError("client not found")
        remaining = reservation.total_amount.amount / 2
        if client.wallet < remaining:
            raise ValueError("insufficient funds")
        client.wallet -= remaining
        reservation.confirmed = True
        self.clients.save(client)
        self.reservations.save(reservation)
        self.payments.add(Payment(client_id=client.id, amount=Money(remaining),
                                  kind="reservation_balance",
                                  reservation_id=reservation_id))

    def cancel_reservation(self, reservation_id: int) -> None:
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            raise ValueError("reservation not found")
        self.reservations.remove(reservation_id)
