-- CREATE TABLE car (
--   id SERIAL PRIMARY KEY,
--   brand VARCHAR(20) NOT NULL,
--   rentprice INT NOT NULL -- цена аренды
-- );

-- CREATE TABLE client (
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(10) NOT NULL,
--   passport VARCHAR(50) NOT NULL,
--   country VARCHAR(50) NOT NULL
-- );

-- CREATE TABLE rentbook (
--   id SERIAL PRIMARY KEY,
--   date DATE NOT NULL, -- дата аренды
--   time INT NOT NULL, -- время на сколько взята аренда в часах
--   paid BOOLEAN NOT NULL, -- TRUE оплатил; FALSE не оплатил
--   carid INT NOT NULL,
--   clientid INT NOT NULL,
--   FOREIGN KEY (carid) REFERENCES car (id),
--   FOREIGN KEY (clientid) REFERENCES client (id)
-- );

-- Second version

-- Dimension Table: cars
CREATE TABLE cars (
  car_id SERIAL PRIMARY KEY,
  brand VARCHAR(20) NOT NULL,
  model VARCHAR(20) NOT NULL,
  year INT NOT NULL,
  rent_price INT NOT NULL, -- цена аренды
  color VARCHAR(20)
);

-- Dimension Table: clients
CREATE TABLE clients (
  client_id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NOT NULL,
  surname VARCHAR(50) NOT NULL,
  passport_series SMALLINT NOT NULL,
  passport_number INTEGER NOT NULL,
  country VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  phone VARCHAR(20)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_passport ON clients (passport_series, passport_number);

-- Dimension Table: payments
CREATE TABLE payments (
  payment_id SERIAL PRIMARY KEY,
  method VARCHAR(20) NOT NULL, -- e.g., cash, credit card, online
  paid BOOLEAN NOT NULL, -- TRUE оплатил; FALSE не оплатил
  amount DECIMAL(10, 2) NOT NULL,
  payment_dttm timestamp NOT NULL DEFAULT current_timestamp
);

-- Fact Table: rent_book
CREATE TABLE rent_book (
  rental_id SERIAL PRIMARY KEY,
  car_id INT NOT NULL,
  client_id INT NOT NULL,
  start_dttm timestamp NOT NULL DEFAULT current_timestamp,
  end_dttm timestamp,
  payment_id INT NOT NULL,
  rental_duration INT NOT NULL, -- duration in hours
  FOREIGN KEY (car_id) REFERENCES cars (car_id),
  FOREIGN KEY (client_id) REFERENCES clients (client_id),
  FOREIGN KEY (payment_id) REFERENCES payments (payment_id)
);
