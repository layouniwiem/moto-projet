from app.app import create_app, db  # Corrigé ici

def test_homepage():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.create_all()

    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    print(response.data.decode())  # Pour debug si le test échoue
    assert b"Moto" in response.data
