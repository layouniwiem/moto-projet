
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
('Honda', 'CBR 600RR', 2018, 15000, 8500, 'Excellent état, entretien régulier',"https://www.bing.com/images/search?q=images%20(%27Honda%27,%20%27CBR%20600RR%27,%202019,%2015000,%208500,%20%27Excellent%20%C3%A9tat,%20entretien%20r%C3%A9gulier%27),&FORM=IQFRBA&id=35C3D9F3EDD45822FE354A8283CC56649922FA00"),
('Yamaha', 'MT-07', 2020, 8000, 6500, 'Première main, comme neuve'),
('Kawasaki', 'Z900', 2021, 5000, 9000, 'Garantie constructeur, options incluses');