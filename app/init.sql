
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
('admin', 'admin@example.com', 'pbkdf2:sha256:260000$hqhdH035aotJ6Xw0$359165cf690ea13c7f64c512078a3df41bdbc366543160b3721e49757fef306c'),
('user1', 'user1@example.com', 'pbkdf2:sha256:260000$hqhdH035aotJ6Xw0$359165cf690ea13c7f64c512078a3df41bdbc366543160b3721e49757fef306c');

-- Insertion de motos de test
INSERT INTO moto (marque, modele, annee, kilometrage, prix, description,image_url) VALUES 
('Honda', 'CBR 600RR', 2018, 15000, 8500, 'Excellent état, entretien régulier', 'https://th.bing.com/th/id/OIP.JbSULy1SSk58Jh9ZOC0vPAHaEo?rs=1&pid=ImgDetMain'),
('Yamaha', 'MT-07', 2020, 8000, 6500, 'Première main, comme neuve', 'https://th.bing.com/th/id/OIP.iSrQVgkeN4nkzHSfPl1eCAHaFj?rs=1&pid=ImgDetMain'),
('Kawasaki', 'Z900', 2021, 5000, 9000, 'Garantie constructeur, options incluses', 'https://th.bing.com/th/id/R.449368898dd81b2ea3f04c993a060cba?rik=fwG96vc7Y2hfDw&pid=ImgRaw&r=0');