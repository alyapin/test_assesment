import psycopg2
import random
import os
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Database connection parameters
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_PORT = 5432
DB_HOST = os.getenv('POSTGRES_HOST')

# Payment methods
payment_methods = ["cash", "credit card", "online"]

# Define the date range for start_dttm
start_date = datetime(2000, 10, 1)
end_date = datetime(2024, 6, 29)

def random_date(start, end):
    """
    Generate a random datetime between `start` and `end`.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_payments_and_rentals(num_payments):
    """
    Generate payment and rental records and insert them into the database.
    """
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info("Database connection established.")

        # Create a cursor object
        cur = conn.cursor()

        # Fetch all rent prices and car_ids from the cars table
        cur.execute("SELECT car_id, rent_price FROM cars")
        cars_data = cur.fetchall()
        logging.info("Fetched cars data from database.")

        # Fetch all client_ids from the clients table
        cur.execute("SELECT client_id FROM clients")
        client_ids = [row[0] for row in cur.fetchall()]
        logging.info("Fetched clients data from database.")

        # Generate payments and rent_book data
        for i in range(num_payments):
            car_id, rent_price = random.choice(cars_data)
            method = random.choice(payment_methods)
            paid = random.choice([True, False])
            # Apply a random multiplier between 1 and 1.5 to the rent_price to get the amount
            rental_duration = random.randint(2, 72)  # Rental duration in hours
            amount = rent_price * rental_duration

            # Insert into payments table
            cur.execute("""
            INSERT INTO payments (method, paid, amount)
            VALUES (%s, %s, %s) RETURNING payment_id
            """, (method, paid, amount))
            
            # Get the payment_id of the inserted row
            payment_id = cur.fetchone()[0]

            # Select a random client_id
            client_id = random.choice(client_ids)

            # Generate random start_dttm and calculate end_dttm
            start_dttm = random_date(start_date, end_date)
            end_dttm = start_dttm + timedelta(hours=rental_duration)

            # Insert into rent_book table
            cur.execute("""
            INSERT INTO rent_book (car_id, client_id, start_dttm, end_dttm, payment_id, rental_duration)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (car_id, client_id, start_dttm, end_dttm, payment_id, rental_duration))

            if (i + 1) % 1000 == 0:  # Log every 1000 records
                logging.info(f"{i + 1} records inserted into payments and rent_book tables.")

        # Commit the transaction
        conn.commit()
        logging.info("Transaction committed to the database.")

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        # Close the cursor and the connection
        if cur:
            cur.close()
            logging.info("Cursor closed.")
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    num_payments = 6000  # Change this to the desired number of payment records
    logging.info(f"Starting generation of {num_payments} payments and rentals.")
    generate_payments_and_rentals(num_payments)
    logging.info("Finished generating payments and rentals.")
