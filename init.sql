
# init.sql
CREATE DATABASE IF NOT EXISTS moto_db;
USE moto_db;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS moto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(50) NOT NULL,
    annee INT NOT NULL,
    kilometrage INT,
    prix FLOAT NOT NULL,
    description TEXT,
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
    image_url VARCHAR(200)
);

-- Insertion d'utilisateurs de test
INSERT INTO user (username, email, password_hash) VALUES 
('admin', 'admin@example.com', 'pbkdf2:sha256:260000$YOUR_HASH_HERE'),
('user1', 'user1@example.com', 'pbkdf2:sha256:260000$YOUR_HASH_HERE');

-- Insertion de motos de test
INSERT INTO moto (marque, modele, annee, kilometrage, prix, description) VALUES 
('Honda', 'CBR 600RR', 2019, 15000, 8500, 'Excellent état, entretien régulier'),
('Yamaha', 'MT-07', 2020, 8000, 6500, 'Première main, comme neuve'),
('Kawasaki', 'Z900', 2021, 5000, 9000, 'Garantie constructeur, options incluses');