import json
import os

RATES_TO_EUR = {
    'EUR': 1.0,
    'USD': 0.9,
    'GBP': 1.15,
    'JPY': 0.007,
    'CHF': 1.0,
}

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.json')


def init_schema():
    """Initialize the JSON database file if it does not exist."""
    if not os.path.exists(DB_PATH):
        data = {
            'clients': [],
            'rooms': [
                {
                    'id': 1,
                    'room_type': 'standard',
                    'price': 50,
                    'description': 'Single bed, Wifi, TV'
                },
                {
                    'id': 2,
                    'room_type': 'superior',
                    'price': 100,
                    'description': 'Double bed, Wifi, flat screen TV, minibar, air conditioner'
                },
                {
                    'id': 3,
                    'room_type': 'suite',
                    'price': 200,
                    'description': 'Double bed, Wifi, flat screen TV, minibar, air conditioner, bathtub, terrace'
                },
            ],
            'reservations': [],
            'payments': [],
            'auto_id': {'client': 0, 'room': 3, 'reservation': 0, 'payment': 0}
        }
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f)


def _load() -> dict:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def _record_payment(data: dict, client_id: int, amount: float, currency: str,
                    kind: str, reservation_id: int | None = None) -> None:
    data['auto_id']['payment'] += 1
    pid = data['auto_id']['payment']
    data.setdefault('payments', [])
    data['payments'].append({
        'id': pid,
        'client_id': client_id,
        'reservation_id': reservation_id,
        'amount': amount,
        'currency': currency,
        'type': kind,
    })


def add_client(full_name: str, email: str, phone: str) -> int:
    """Add a new client if the email is not already registered."""
    init_schema()
    data = _load()
    if any(c['email'] == email for c in data['clients']):
        raise ValueError("client already exists")
    data['auto_id']['client'] += 1
    cid = data['auto_id']['client']
    data['clients'].append({
        'id': cid,
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'wallet': 0.0,
    })
    _save(data)
    return cid


def deposit(client_id: int, amount: float, currency: str = 'EUR') -> float:
    """Credit a client's wallet and return the new balance."""
    init_schema()
    data = _load()
    client = next((c for c in data['clients'] if c['id'] == client_id), None)
    if client is None:
        raise ValueError('client not found')
    if 'wallet' not in client:
        raise ValueError('client wallet not initialized')
    rate = RATES_TO_EUR.get(currency.upper())
    if rate is None:
        raise ValueError('unsupported currency')
    client['wallet'] += amount * rate
    _record_payment(data, client_id, amount, currency.upper(), 'deposit')
    _save(data)
    return client['wallet']


def add_room(room_type: str, price: float, description: str) -> int:
    init_schema()
    data = _load()
    data['auto_id']['room'] += 1
    rid = data['auto_id']['room']
    data['rooms'].append({'id': rid, 'room_type': room_type, 'price': price, 'description': description})
    _save(data)
    return rid


def add_reservation(client_id: int, room_id: int, check_in: str, nights: int) -> int:
    init_schema()
    data = _load()
    client = next((c for c in data['clients'] if c['id'] == client_id), None)
    if client is None:
        raise ValueError('client not found')
    if 'wallet' not in client:
        raise ValueError('client wallet not initialized')

    from datetime import datetime, timedelta
    new_start = datetime.fromisoformat(check_in)
    new_end = new_start + timedelta(days=nights)
    for r in data['reservations']:
        if r['room_id'] != room_id:
            continue
        existing_start = datetime.fromisoformat(r['check_in'])
        existing_end = existing_start + timedelta(days=r['nights'])
        if new_start < existing_end and new_end > existing_start:
            raise ValueError('room not available for the selected dates')

    room = next((r for r in data['rooms'] if r['id'] == room_id), None)
    if room is None:
        raise ValueError('room not found')
    total = room['price'] * nights
    deposit_amount = total / 2
    if client['wallet'] < deposit_amount:
        raise ValueError('insufficient funds')
    data['auto_id']['reservation'] += 1
    rid = data['auto_id']['reservation']
    client['wallet'] -= deposit_amount
    _record_payment(data, client_id, deposit_amount, 'EUR',
                    'reservation_deposit', rid)
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


def list_rooms() -> list:
    init_schema()
    data = _load()
    return data['rooms']


def confirm_reservation(reservation_id: int) -> None:
    """Mark an existing reservation as confirmed."""
    init_schema()
    data = _load()
    for r in data['reservations']:
        if r['id'] == reservation_id:
            if r['confirmed']:
                return
            client = next((c for c in data['clients'] if c['id'] == r['client_id']), None)
            if client is None:
                raise ValueError('client not found')
            if 'wallet' not in client:
                raise ValueError('client wallet not initialized')
            remaining = r['total'] / 2
            if client['wallet'] < remaining:
                raise ValueError('insufficient funds')
            client['wallet'] -= remaining
            _record_payment(data, client['id'], remaining, 'EUR',
                            'reservation_balance', r['id'])
            r['confirmed'] = True
            _save(data)
            return
    raise ValueError("reservation not found")


def cancel_reservation(reservation_id: int) -> None:
    """Cancel (delete) an existing reservation."""
    init_schema()
    data = _load()
    before = len(data['reservations'])
    data['reservations'] = [r for r in data['reservations'] if r['id'] != reservation_id]
    if len(data['reservations']) == before:
        raise ValueError("reservation not found")
    _save(data)
