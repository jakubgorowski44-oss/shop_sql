-- =========================
-- CLIENTS
-- =========================
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    address TEXT NOT NULL
);

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price NUMERIC(10,2) NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    clients_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_clients
        FOREIGN KEY (clients_id)
        REFERENCES clients(id)
        ON DELETE CASCADE
);

-- =========================
-- ORDER ITEMS (M:N)
-- =========================
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_items_product
        FOREIGN KEY (products_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
);