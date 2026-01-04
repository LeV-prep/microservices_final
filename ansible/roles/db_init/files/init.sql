CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO products (name, price) VALUES
  ('T-shirt DevOps', 19.99),
  ('Mug Terraform', 12.50),
  ('Sticker Kubernetes', 3.00)
ON CONFLICT DO NOTHING;

INSERT INTO users (username, password) VALUES
  ('victor', 'test123'),
  ('admin', 'admin123')
ON CONFLICT (username) DO NOTHING;
