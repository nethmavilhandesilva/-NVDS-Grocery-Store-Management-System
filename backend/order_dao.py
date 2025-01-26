from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table
    order_query = (
        "INSERT INTO orders (customer_name, Total, date_time) VALUES (%s, %s, %s)"
    )
    order_data = (order['customer_name'], order['grand_total'], datetime.now())
    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    # Insert into order_details table
    order_details_query = (
        "INSERT INTO order_details (order_id, product_id, qantity, Total) VALUES (%s, %s, %s, %s)"
    )
    order_details_data = []

    # Check for duplicates in the order details
    seen_products = set()  # To track product IDs for the current order
    for order_details_record in order['order_details']:
        product_id = int(order_details_record['product_id'])

        if product_id in seen_products:
            # Avoid duplicate entries for the same product
            continue

        seen_products.add(product_id)
        order_details_data.append([
            order_id,
            product_id,
            float(order_details_record['quantity']),
            float(order_details_record['total_price']),
        ])

    # Execute batch insert
    if order_details_data:
        cursor.executemany(order_details_query, order_details_data)

    connection.commit()
    return order_id

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * from orders")
    cursor.execute(query)

    response = []
    for (order_id, customer_name, total,datetime) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name':customer_name,
            'total':total,
            'datetime':datetime
        })


if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'Sandini',
        'grand_total': '500',
        'order_details': [
            {
                'product_id': 2,
                'quantity': 2,
                'total_price': 50
            },
            {
                'product_id': 2,  # Duplicate product_id
                'quantity': 2,
                'total_price': 50
            },
        ]
    }))
