-- Top 5 Most Rented Car Models by Quarterly Rental Counts
WITH quarterly_rentals AS (
  SELECT
    c.brand || ' ' || c.model AS car_model,
    EXTRACT(YEAR FROM rb.start_dttm) AS rental_year,
    EXTRACT(QUARTER FROM rb.start_dttm) AS rental_quarter,
    COUNT(rb.rental_id) AS rental_count,
    ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM rb.start_dttm), EXTRACT(QUARTER FROM rb.start_dttm) ORDER BY COUNT(rb.rental_id) DESC) AS quarter_rank
  FROM
    rent_book rb
  JOIN
    cars c ON rb.car_id = c.car_id
  GROUP BY
    car_model, rental_year, rental_quarter
)
SELECT
  car_model,
  rental_year,
  rental_quarter,
  rental_count
FROM
  quarterly_rentals
WHERE
  quarter_rank <= 5
ORDER BY
  rental_year, rental_quarter, quarter_rank;


-- Monthly Revenue Trend for the Current Year
SELECT
  EXTRACT(MONTH FROM rb.start_dttm) AS rental_month,
  COALESCE(SUM(p.amount), 0) AS total_revenue
FROM
  rent_book rb
LEFT JOIN (
  SELECT
    payment_id,
    amount
  FROM
    payments
  WHERE
    paid = TRUE
) AS p ON rb.payment_id = p.payment_id
WHERE
  EXTRACT(YEAR FROM rb.start_dttm) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY
  rental_month
ORDER BY
  rental_month;

-- Total revenue by cars
SELECT
  c.brand,
  c.model,
  SUM(p.amount) AS total_revenue
FROM
  rent_book rb
JOIN
  cars c ON rb.car_id = c.car_id
JOIN
  payments p ON rb.payment_id = p.payment_id
WHERE
  p.paid = TRUE
GROUP BY
  c.brand, c.model
ORDER BY
  total_revenue DESC;

-- Monthly Revenue Comparison with Previous Year
WITH monthly_revenue AS (
  SELECT
    EXTRACT(YEAR FROM rb.start_dttm) AS rental_year,
    EXTRACT(MONTH FROM rb.start_dttm) AS rental_month,
    SUM(p.amount) AS total_revenue
  FROM
    rent_book rb
  JOIN
    payments p ON rb.payment_id = p.payment_id
  WHERE
    p.paid = TRUE
  GROUP BY
    rental_year, rental_month
)
select
  rental_year,
  rental_month,
  total_revenue,
  coalesce(lag(total_revenue) over w, 0) prev_year_total_revenue,
  coalesce(lag(rental_year) over w, rental_year - 1)prev_rental_year
from monthly_revenue
window w as(
  partition by rental_month order by rental_year
);

-- Clients with Highest Total Spend
SELECT
  cl.name || ' ' || cl.surname client,
  SUM(p.amount) AS total_spent
FROM
  clients cl
JOIN
  rent_book rb ON cl.client_id = rb.client_id
JOIN
  payments p ON rb.payment_id = p.payment_id
WHERE
  p.paid = TRUE
GROUP BY
  cl.client_id, cl.name, cl.surname
ORDER BY
  total_spent DESC
LIMIT 100;

