import json
import os

from domain.entities import Client, Room, Reservation, Payment
from domain.value_objects import Money, Currency
from domain.repositories import (
    ClientRepository,
    RoomRepository,
    ReservationRepository,
    PaymentRepository,
)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.json')


def _load() -> dict:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def init_schema() -> None:
    if os.path.exists(DB_PATH):
        return
    data = {
        'clients': [],
        'rooms': [
            {'id': 1, 'room_type': 'standard', 'price': 50, 'description': 'Single bed, Wifi, TV'},
            {'id': 2, 'room_type': 'superior', 'price': 100, 'description': 'Double bed, Wifi, flat screen TV, minibar, air conditioner'},
            {'id': 3, 'room_type': 'suite', 'price': 200, 'description': 'Double bed, Wifi, flat screen TV, minibar, air conditioner, bathtub, terrace'},
        ],
        'reservations': [],
        'payments': [],
        'auto_id': {'client': 0, 'room': 3, 'reservation': 0, 'payment': 0}
    }
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)


class JsonClientRepository(ClientRepository):
    def add(self, client: Client) -> None:
        data = _load()
        data['auto_id']['client'] += 1
        client.id = data['auto_id']['client']
        data['clients'].append({'id': client.id, 'full_name': client.full_name,
                                'email': client.email, 'phone': client.phone,
                                'wallet': client.wallet})
        _save(data)

    def get(self, client_id: int) -> Client | None:
        data = _load()
        d = next((c for c in data['clients'] if c['id'] == client_id), None)
        if not d:
            return None
        return Client(d['full_name'], d['email'], d['phone'], wallet=d.get('wallet', 0.0), id=d['id'])

    def find_by_email(self, email: str) -> Client | None:
        data = _load()
        d = next((c for c in data['clients'] if c['email'] == email), None)
        if not d:
            return None
        return Client(d['full_name'], d['email'], d['phone'], wallet=d.get('wallet', 0.0), id=d['id'])

    def save(self, client: Client) -> None:
        data = _load()
        for c in data['clients']:
            if c['id'] == client.id:
                c['full_name'] = client.full_name
                c['email'] = client.email
                c['phone'] = client.phone
                c['wallet'] = client.wallet
                break
        _save(data)


class JsonRoomRepository(RoomRepository):
    def add(self, room: Room) -> None:
        data = _load()
        data['auto_id']['room'] += 1
        room.id = data['auto_id']['room']
        data['rooms'].append({'id': room.id, 'room_type': room.room_type,
                              'price': room.price_per_night.amount,
                              'description': room.description})
        _save(data)

    def get(self, room_id: int) -> Room | None:
        data = _load()
        d = next((r for r in data['rooms'] if r['id'] == room_id), None)
        if not d:
            return None
        return Room(d['room_type'], Money(d['price']), d['description'], id=d['id'])

    def list(self) -> list[Room]:
        data = _load()
        return [Room(r['room_type'], Money(r['price']), r['description'], id=r['id']) for r in data['rooms']]


class JsonReservationRepository(ReservationRepository):
    def add(self, reservation: Reservation) -> None:
        data = _load()
        data['auto_id']['reservation'] += 1
        reservation.id = data['auto_id']['reservation']
        data['reservations'].append({
            'id': reservation.id,
            'client_id': reservation.client_id,
            'room_id': reservation.room_id,
            'check_in': reservation.check_in,
            'nights': reservation.nights,
            'total': reservation.total_amount.amount,
            'confirmed': reservation.confirmed,
        })
        _save(data)

    def get(self, reservation_id: int) -> Reservation | None:
        data = _load()
        d = next((r for r in data['reservations'] if r['id'] == reservation_id), None)
        if not d:
            return None
        return Reservation(d['client_id'], d['room_id'], d['check_in'], d['nights'],
                           Money(d['total']), confirmed=d['confirmed'], id=d['id'])

    def list(self) -> list[Reservation]:
        data = _load()
        return [Reservation(r['client_id'], r['room_id'], r['check_in'], r['nights'],
                            Money(r['total']), confirmed=r['confirmed'], id=r['id'])
                for r in data['reservations']]

    def remove(self, reservation_id: int) -> None:
        data = _load()
        before = len(data['reservations'])
        data['reservations'] = [r for r in data['reservations'] if r['id'] != reservation_id]
        if len(data['reservations']) == before:
            raise ValueError('reservation not found')
        _save(data)

    def save(self, reservation: Reservation) -> None:
        data = _load()
        for r in data['reservations']:
            if r['id'] == reservation.id:
                r['confirmed'] = reservation.confirmed
                break
        _save(data)


class JsonPaymentRepository(PaymentRepository):
    def add(self, payment: Payment) -> None:
        data = _load()
        data['auto_id']['payment'] += 1
        payment.id = data['auto_id']['payment']
        data.setdefault('payments', [])
        data['payments'].append({
            'id': payment.id,
            'client_id': payment.client_id,
            'reservation_id': payment.reservation_id,
            'amount': payment.amount.amount,
            'currency': payment.amount.currency.value,
            'type': payment.kind,
        })
        _save(data)

    def list_for_client(self, client_id: int) -> list[Payment]:
        data = _load()
        return [Payment(p['client_id'], Money(p['amount'], Currency(p['currency'])), p['type'], p.get('reservation_id'), id=p['id'])
                for p in data.get('payments', []) if p['client_id'] == client_id]

