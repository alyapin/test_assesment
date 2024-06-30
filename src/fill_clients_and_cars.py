import pandas as pd
from sqlalchemy import create_engine
import random
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to generate unique passport series and number
def generate_passport():
    return random.randint(1000, 9999), random.randint(100000, 999999)

# Function to generate client data
def generate_client_data(names_df, countries_df, num_rows):
    data = []
    passport_numbers = set()
    while len(data) < num_rows:
        name_row = random.choice(names_df.index)
        middle_name_row = random.choice(names_df.index)
        surname_row = random.choice(names_df.index)
        
        name = names_df.loc[name_row, 'name']
        middle_name = names_df.loc[middle_name_row, 'middle_name']
        surname = names_df.loc[surname_row, 'surname']
        
        passport_series, passport_number = generate_passport()
        passport_union = f"{passport_series}-{passport_number}"
        if passport_union in passport_numbers:
            continue
        passport_numbers.add(passport_union)

        country_row = random.choice(countries_df.index)
        country = countries_df.loc[country_row, 'country']

        data.append((name, middle_name, surname, passport_series, passport_number, country))

    return pd.DataFrame(data, columns=['name', 'middle_name', 'surname', 'passport_series', 'passport_number', 'country'])

# Function to insert data into PostgreSQL table
def insert_into_postgres(df, db_url, table_name):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logging.info(f"Data inserted successfully into PostgreSQL table {table_name}.")
    except Exception as e:
        logging.error(f"Error inserting data into PostgreSQL table {table_name}: {str(e)}")

# Main script execution
if __name__ == "__main__":
    # Read names.csv and countries.csv into Pandas DataFrames
    names_df = pd.read_csv('data/names.csv')
    countries_df = pd.read_csv('data/countries.csv')
    cars_df = pd.read_csv('data/cars_data.csv')

    # Generate client data
    num_rows = 10000
    client_df = generate_client_data(names_df, countries_df, num_rows)

    # Display some sample client data
    logging.info(f"Generated sample client data:\n{client_df.head()}")

    db_url = os.getenv('DATABASE_URL')

    table_name_clients = 'clients'
    table_name_cars = 'cars'
    
    # db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    insert_into_postgres(client_df, db_url, table_name_clients)
    insert_into_postgres(cars_df, db_url, table_name_cars)