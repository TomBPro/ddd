import argparse

from . import db


def cmd_init(_args):
    db.init_schema()
    print("Database initialized")


def cmd_add_client(args):
    try:
        cid = db.add_client(args.name, args.email, args.phone)
    except ValueError as e:
        print(str(e))
        return
    print(f"Client added with id {cid}")


def cmd_add_room(args):
    rid = db.add_room(args.type, args.price)
    print(f"Room added with id {rid}")


def cmd_reserve(args):
    try:
        rid = db.add_reservation(args.client, args.room, args.check_in, args.nights, args.total)
        print(f"Reservation created with id {rid}")
    except ValueError as e:
        print(str(e))


def cmd_list_rooms(_args):
    rooms = db.list_rooms()
    for r in rooms:
        print(f"{r['id']}: {r['room_type']} - {r['price']}€ - {r['description']}")


def cmd_confirm(args):
    try:
        db.confirm_reservation(args.reservation)
        print(f"Reservation {args.reservation} confirmed")
    except ValueError as e:
        print(str(e))


def cmd_cancel(args):
    try:
        db.cancel_reservation(args.reservation)
        print(f"Reservation {args.reservation} cancelled")
    except ValueError as e:
        print(str(e))


def cmd_deposit(args):
    try:
        balance = db.deposit(args.client, args.amount, args.currency)
        print(f"New balance: {balance:.2f} EUR")
    except ValueError as e:
        print(str(e))


def main(argv=None):
    parser = argparse.ArgumentParser(description="XYZ Hotel CLI")
    sub = parser.add_subparsers(dest="command")

    init_p = sub.add_parser("init-db")
    init_p.set_defaults(func=cmd_init)

    add_client_p = sub.add_parser("add-client")
    add_client_p.add_argument("--name", required=True)
    add_client_p.add_argument("--email", required=True)
    add_client_p.add_argument("--phone", required=True)
    add_client_p.set_defaults(func=cmd_add_client)

    add_room_p = sub.add_parser("add-room")
    add_room_p.add_argument("--type", required=True)
    add_room_p.add_argument("--price", type=float, required=True)
    add_room_p.set_defaults(func=cmd_add_room)

    list_rooms_p = sub.add_parser("list-rooms")
    list_rooms_p.set_defaults(func=cmd_list_rooms)

    res_p = sub.add_parser("reserve")
    res_p.add_argument("--client", type=int, required=True)
    res_p.add_argument("--room", type=int, required=True)
    res_p.add_argument("--check-in", required=True)
    res_p.add_argument("--nights", type=int, required=True)
    res_p.add_argument("--total", type=float, required=True)
    res_p.set_defaults(func=cmd_reserve)

    confirm_p = sub.add_parser("confirm")
    confirm_p.add_argument("--reservation", type=int, required=True)
    confirm_p.set_defaults(func=cmd_confirm)

    cancel_p = sub.add_parser("cancel")
    cancel_p.add_argument("--reservation", type=int, required=True)
    cancel_p.set_defaults(func=cmd_cancel)

    deposit_p = sub.add_parser("deposit")
    deposit_p.add_argument("--client", type=int, required=True)
    deposit_p.add_argument("--amount", type=float, required=True)
    deposit_p.add_argument("--currency", default="EUR")
    deposit_p.set_defaults(func=cmd_deposit)

    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
