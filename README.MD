# Rendu

## Tactical Design

### Entities



### Value Objects



### How to run the code & tests

```bash
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
