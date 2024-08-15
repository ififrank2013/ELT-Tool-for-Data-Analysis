-- Created a schema to hold e-commerce data tables
CREATE SCHEMA IF NOT EXISTS ecommerce;

-- Creating tables based on dataset schema
CREATE TABLE IF NOT EXISTS ecommerce.geolocation (
  geolocation_zip_code_prefix INT PRIMARY KEY,
  geolocation_lat NUMERIC,
  geolocation_lng NUMERIC,
  geolocation_city VARCHAR,
  geolocation_state VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce.customers (
  customer_id VARCHAR PRIMARY KEY,
  customer_unique_id VARCHAR,
  customer_zip_code_prefix INT REFERENCES ecommerce.geolocation(geolocation_zip_code_prefix),
  customer_city VARCHAR,
  customer_state VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce.orders (
  order_id VARCHAR PRIMARY KEY,
  customer_id VARCHAR REFERENCES ecommerce.customers(customer_id),
  order_status VARCHAR,
  order_purchase_timestamp TIMESTAMP,
  order_approved_at TIMESTAMP,
  order_delivered_carrier_date TIMESTAMP,
  order_delivered_customer_date TIMESTAMP,
  order_estimated_delivery_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce.products (
  product_id VARCHAR PRIMARY KEY,
  product_category_name VARCHAR,
  product_name_length INT,
  product_description_length INT,
  product_photos_qty INT,
  product_weight_g INT,
  product_length_cm INT,
  product_height_cm INT,
  product_width_cm INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce.sellers (
  seller_id VARCHAR PRIMARY KEY,
  seller_zip_code_prefix INT REFERENCES ecommerce.geolocation(geolocation_zip_code_prefix),
  seller_city VARCHAR,
  seller_state VARCHAR,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ecommerce.order_items (
  order_id VARCHAR REFERENCES ecommerce.orders(order_id),
  order_item_id INT,
  product_id VARCHAR REFERENCES ecommerce.products(product_id),
  seller_id VARCHAR REFERENCES ecommerce.sellers(seller_id),
  shipping_limit_date TIMESTAMP,
  price NUMERIC,
  freight_value NUMERIC,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS ecommerce.order_payments (
  order_id VARCHAR REFERENCES ecommerce.orders(order_id),
  payment_sequence INT,
  payment_type VARCHAR,
  payment_installments INT,
  payment_value NUMERIC,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id, payment_sequence)
);

CREATE TABLE IF NOT EXISTS ecommerce.order_reviews (
  review_id VARCHAR PRIMARY KEY,
  order_id VARCHAR REFERENCES ecommerce.orders(order_id),
  review_score INT,
  review_comment_title VARCHAR,
  review_comment_message VARCHAR,
  review_creation_date TIMESTAMP,
  review_answer_timestamp TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
