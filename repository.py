from database import conn
def add_client():
    cursor = conn.cursor()  
    try:
        client = {
        'name' : input("Enter name: "),
        'lastname' : input("Enter lastname: "),
        'address' : input("Enter address: ")
        }
        for k, v in client.items():
            if not v.strip():
                print(f"Wrong data: {k}")
                return
        cursor.execute('INSERT INTO clients(name,lastname,address) VALUES(%(name)s, %(lastname)s, %(address)s)', client)
        conn.commit()
        print("Client added.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
            
def show_clients():
    cursor = conn.cursor()  
    try:
        cursor.execute('SELECT id, name, lastname, address FROM clients')
        for row in cursor:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()  

def delete_client():
    cursor = conn.cursor()
    show_clients()
    try:
        try:
            id = int(input("Enter client's id to remove: "))
        except ValueError:
            return
        cursor.execute("DELETE FROM clients WHERE id = %s",(id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

def add_product():
    cursor = conn.cursor()  
    try:
        while True:
            try:
                product = {
                'name' : input("Enter name: "),
                'price' : float(input("Enter price: ")),
                'stock' : int(input("Enter stock: "))
                }
                break
            except (ValueError, TypeError):
                print("Wrong value! Try again.")
        if not product['name'].strip():
            print("Wrong product name.")
            return
        for k, v in product.items():
            if v is None:
                print(f"Wrong data: {k}")
                return
        if product['price'] <= 0:
            print("Price must be greater than 0")
            return
        if product['stock'] < 0:
            print("Stock cannot be negative")
            return
        cursor.execute('INSERT INTO products(name,price,stock) VALUES(%(name)s, %(price)s, %(stock)s)', product)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()       

def show_products():
    cursor = conn.cursor() 
    try: 
        cursor.execute('SELECT id, name, price, stock FROM products')
        for row in cursor:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def delete_product():
    cursor = conn.cursor()
    show_products()
    try:
        try:
            id = int(input("Enter product id to remove: "))
        except ValueError:
            return
        cursor.execute("DELETE FROM products WHERE id = %s",(id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

def make_order():
    cursor = conn.cursor()
    show_clients()
    try:
        try:
            client_id = int(input("Enter client id: "))
        except ValueError:
            return
        
        cursor.execute(
        "SELECT id FROM clients WHERE id = %s",
        (client_id,)
        )

        if cursor.fetchone() is None:
            print("Client does not exist.")
            return
        
        cursor.execute(
        "INSERT INTO orders(clients_id) VALUES (%s) RETURNING id",
        (client_id,)
        )

        row = cursor.fetchone()

        if row is None:
            print("INSERT failed - no row returned")
            return

        order_id = row[0]
        items_added = False
        while True:
            show_products()
            try:
                product_id = int(input("Product id (0 to stop): "))
                if product_id == 0:
                    break

                quantity = int(input("Quantity: "))

            except ValueError:
                print("Wrong value")
                continue
            cursor.execute('SELECT stock FROM products WHERE id = %s',
                           (product_id,))
            row = cursor.fetchone()
            if row is None:
                print("Product does not exist.")
                continue
            stock = row[0]
            if quantity > stock:
                print(f"Not enough stock. Available: {stock}")
                continue
            if quantity <= 0:
                print("Quantity must be greater than 0")
                continue
            cursor.execute(
                "INSERT INTO order_items(order_id, products_id, quantity) VALUES (%s, %s, %s)",
                (order_id, product_id, quantity)
            )
            cursor.execute('UPDATE products SET stock = stock - %s WHERE id = %s',
                           (quantity, product_id)
                           )
            items_added = True
        if not items_added:
            conn.rollback()
            print("Order must contain at least one product")
            return

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()

def show_orders():
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM orders')
        for row in cursor:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def delete_order():
    cursor = conn.cursor()
    show_orders()
    try:
        try:
            order_id = int(input("Enter order id to remove: "))
        except ValueError:
            return
        cursor.execute('SELECT products_id, quantity '
        'FROM order_items '
        'WHERE order_id = %s',(order_id,))

        items = cursor.fetchall()

        if not items:
            print("Order does not exist.")
            return

        for product_id, quantity in items:
            cursor.execute('UPDATE products '
            'SET stock = stock + %s '
            'WHERE id = %s',(quantity,product_id))

        cursor.execute("DELETE FROM orders WHERE id = %s",(order_id,))
        conn.commit()
        print("Order removed.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close() 

def report():
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT '
        'p.name, '
        'SUM(oi.quantity) AS sold '
        'FROM products p '
        'JOIN order_items oi '
        'ON p.id = oi.products_id '
        'GROUP BY p.id, p.name '
        'ORDER BY sold DESC;')
        for row in cursor:
            print(f"{row[0]} - {row[1]}")
        cursor.execute('SELECT c.name,address, SUM(p.price * oi.quantity) '
        'FROM orders o '
        'JOIN clients c ON c.id = o.clients_id '
        'JOIN order_items oi ON oi.order_id = o.id '
        'JOIN products p ON p.id = oi.products_id '
        'GROUP BY c.id,c.name,address '
        'ORDER BY SUM(p.price * oi.quantity) DESC')
        for row in cursor:
            print(f"{row[0]} from {row[1]} spend {row[2]}$")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()