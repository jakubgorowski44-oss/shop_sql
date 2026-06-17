# Console Shop Management System

## Overview

Console Shop Management System is a Python application for managing a simple shop database using PostgreSQL. The program allows users to manage clients, products, and orders through a command-line interface.

The project was created for learning:

* Python database programming
* PostgreSQL
* SQL queries
* Table relationships
* Foreign keys
* Data aggregation and reporting
* Environment variables with `.env`

---

## Features

### Client Management

* Add new clients
* Display all clients
* Delete clients

Stored client information:

* First name
* Last name
* Address

### Product Management

* Add new products
* Display available products
* Delete products

Stored product information:

* Product name
* Price
* Stock quantity

### Order Management

* Create orders for existing clients
* Add multiple products to an order
* Display all orders
* Delete orders

### Sales Reports

Generate reports showing:

* Client name
* Client address
* Total amount spent

Results are sorted by highest spending customers.

---

## Technologies

* Python 3
* PostgreSQL
* psycopg2
* python-dotenv

---

## Project Structure

```text
project/
│
├── main.py          # Console menu
├── database.py      # Database connection
├── repository.py    # Database operations
├── .env             # Database configuration
├── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd project
```

### 2. Install dependencies

```bash
pip install psycopg2-binary python-dotenv
```

---

## Database Configuration

Create a `.env` file:

```env
DB_NAME=shop_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Database Schema

### Clients

```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL
);
```

### Products

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL
);
```

### Orders

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    clients_id INTEGER REFERENCES clients(id)
);
```

### Order Items

```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    products_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL
);
```

---

## Running the Application

Start the application:

```bash
python main.py
```

The main menu will allow you to manage clients, products, orders, and reports.

---

## Example Report

```text
John from New York spend 150.00$
Mike from Chicago spend 95.50$
Anna from London spend 50.00$
```

---

## Learning Objectives

This project demonstrates:

* Connecting Python to PostgreSQL
* Executing SQL queries with psycopg2
* INSERT, SELECT and DELETE operations
* JOIN queries
* Aggregate functions (SUM)
* GROUP BY and ORDER BY
* Environment variable management
* Basic CRUD operations

---

## Future Improvements

* Update clients and products
* Product stock validation during orders
* Order details view
* Transaction handling
* Better input validation
* Exception handling
* Unit tests
* Object-oriented design
* Logging system

---

## Author

Jakub Górowski

Educational project created to practice Python and PostgreSQL database development.
