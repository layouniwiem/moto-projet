from app import create_app, db
from app.models import Moto  # Assure-toi que le modèle Moto est bien importé ici
from datetime import datetime

def test_homepage():
    app = create_app()

    # Configuration pour le test
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)
        db.create_all()

        # ➕ Ajout d'une moto de test
        moto = Moto(
            marque="Yamaha",
            modele="MT-07",
            annee=2021,
            kilometrage=5000,
            prix=7000,
            description="Moto en très bon état",
            date_ajout=datetime.utcnow(),
            image_url="https://exemple.com/moto.jpg"
        )
        db.session.add(moto)
        db.session.commit()

    # ➕ Simulation d'une requête client
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        html = response.data.decode()

        # Vérifications basiques
        assert "Yamaha" in html
        assert "MT-07" in html
        assert "Moto en très bon état" in html
