import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.json')


def init_schema():
    """Initialize the JSON database file if it does not exist."""
    if not os.path.exists(DB_PATH):
        data = {
            'clients': [],
            'rooms': [],
            'reservations': [],
            'auto_id': {'client': 0, 'room': 0, 'reservation': 0}
        }
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f)


def _load() -> dict:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def add_client(full_name: str, email: str, phone: str) -> int:
    init_schema()
    data = _load()
    data['auto_id']['client'] += 1
    cid = data['auto_id']['client']
    data['clients'].append({'id': cid, 'full_name': full_name, 'email': email, 'phone': phone})
    _save(data)
    return cid


def add_room(room_type: str, price: float) -> int:
    init_schema()
    data = _load()
    data['auto_id']['room'] += 1
    rid = data['auto_id']['room']
    data['rooms'].append({'id': rid, 'room_type': room_type, 'price': price})
    _save(data)
    return rid


def add_reservation(client_id: int, room_id: int, check_in: str, nights: int, total: float) -> int:
    init_schema()
    data = _load()
    data['auto_id']['reservation'] += 1
    rid = data['auto_id']['reservation']
    data['reservations'].append({
        'id': rid,
        'client_id': client_id,
        'room_id': room_id,
        'check_in': check_in,
        'nights': nights,
        'total': total,
        'confirmed': False
    })
    _save(data)
    return rid
