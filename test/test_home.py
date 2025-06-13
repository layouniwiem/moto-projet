from app import create_app, db
import os

def test_homepage():
    app = create_app()
    
    # Patch la config *après* création
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)
       # db.create_all()

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"Motos" in response.data  # Ajuste ce contenu
