import argparse

from . import db


def cmd_init(_args):
    db.init_schema()
    print("Database initialized")


def cmd_add_client(args):
    cid = db.add_client(args.name, args.email, args.phone)
    print(f"Client added with id {cid}")


def cmd_add_room(args):
    rid = db.add_room(args.type, args.price)
    print(f"Room added with id {rid}")


def cmd_reserve(args):
    rid = db.add_reservation(args.client, args.room, args.check_in, args.nights, args.total)
    print(f"Reservation created with id {rid}")


def cmd_list_rooms(_args):
    rooms = db.list_rooms()
    for r in rooms:
        print(f"{r['id']}: {r['room_type']} - {r['price']}€")


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

    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
