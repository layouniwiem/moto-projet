from app import create_app,db

#def test_homepage():
 #   app = create_app()
  #  client = app.test_client()
   # response = client.get('/')
    #assert response.status_code == 200
    #assert b"Motos" in response.data  # Ajuste selon le contenu attendu
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
