# Rendu

## Tactical Design

### Entities

* **Client** – created account of a person using the system.
* **Room** – lodging option available for reservation.
* **Reservation** – booking made by a client for a room and dates.
* **Payment** – money transfer linked to a reservation.
* **Wallet** – electronic wallet tied to a client and holding a balance.

### Value Objects

* **Money** – amount coupled with a currency.
* **Currency** – enumeration of the allowed currencies.
* **RoomType** – standard, superior or suite.

### How to run the code & tests

```bash
# data is stored in database.json in the project root
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# initialize the JSON database
python3 main.py init-db

# run the automated tests
python3 -m unittest discover -s tests
```

## Strategic Design

> Please install [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) to visualize the diagrams in VS Code.

### Ubiquitous language

* **Client** – person who can create an account and reserve rooms.
* **Account** – personal data containing full name, email and phone.
* **Wallet** – electronic wallet tied to a client; holds a balance in euros.
* **Currency** – allowed currencies: EUR, USD, GBP, JPY, CHF.
* **Room** – lodging option; standard, superior or suite with price per night.
* **Reservation** – booking of one or more rooms from a check-in date for a number of nights.
* **Payment** – debit from the wallet for a reservation.

### Bounded Contexts

```mermaid
graph TD
    subgraph Account
        A[Account Management]
    end
    subgraph Wallet
        W[Wallet Operations]
    end
    subgraph Catalog
        C[Room Catalog]
    end
    subgraph Reservation
        R[Reservation Management]
    end
```

### Context maps

```mermaid
graph TD
    Account -- provides clientId --> Wallet
    Account -- provides clientId --> Reservation
    Catalog -- exposes room data --> Reservation
    Wallet -- authorizes payment --> Reservation
```

### Core / Supporting / Generic domains

* **Core:** Reservation Management
* **Supporting:** Room Catalog, Wallet Operations
* **Generic:** Account Management

## Preloaded rooms

`init-db` creates three rooms in the catalog:

* **Standard room** – 50€ per night
  * Single bed
  * Wifi
  * TV
* **Superior room** – 100€ per night
  * Double bed
  * Wifi
  * Flat screen TV
  * Minibar
  * Air conditioner
* **Suite** – 200€ per night
  * Double bed
  * Wifi
  * Flat screen TV
  * Minibar
  * Air conditioner
  * Bathtub
  * Terrace

The wallet balance is always stored in euros. A conversion will therefore be applied if a client pays in another currency.

## CLI commands

All features of the application are exposed through `main.py`:

```bash
python3 main.py init-db                    # initialize the database
python3 main.py add-client --name NAME --email EMAIL --phone PHONE
python3 main.py add-room --type TYPE --price PRICE
python3 main.py list-rooms                 # display all rooms
python3 main.py deposit --client ID --amount AMOUNT [--currency CUR]
python3 main.py reserve --client ID --room ID --check-in DATE --nights N --total TOTAL
python3 main.py confirm --reservation ID
python3 main.py cancel --reservation ID
```

## Example commands with Tom

```bash
# initialize the database and rooms
python3 main.py init-db

# list all available rooms
python3 main.py list-rooms

# register Tom as a client
python3 main.py add-client --name "Tom" --email tom@example.com --phone 0600000000

# add funds to Tom's wallet in dollars
python3 main.py deposit --client 1 --amount 120 --currency USD

# Tom reserves the standard room for two nights starting on 2025-06-01
python3 main.py reserve --client 1 --room 1 --check-in 2025-06-01 --nights 2 --total 100
```
