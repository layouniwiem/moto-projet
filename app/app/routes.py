import os
from flask import (
    Blueprint, jsonify, render_template, redirect,
    url_for, flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image

from .models import User, Moto
from .forms import AddMotoForm, LoginForm
from . import db

# Configuration upload
UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Vérifie si le fichier est une image autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Déclaration des blueprints
main = Blueprint('main', __name__, static_folder='static', template_folder='templates')
auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

# Endpoint de health check (pour Kubernetes)
@main.route('/health')
def health_check():
    return jsonify({"status": "ok"}), 200

# Page d'accueil
@main.route('/')
def home():
    motos = Moto.query.order_by(Moto.date_ajout.desc()).all()
    return render_template('home.html', motos=motos)

# Détail d’une moto
@main.route('/moto/<int:id>')
def moto_details(id):
    moto = Moto.query.get_or_404(id)
    return render_template('moto_details.html', moto=moto)

# Connexion
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        flash('Nom d\'utilisateur ou mot de passe incorrect')
    return render_template('login.html', form=form)

# Déconnexion
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Ajout d'une nouvelle moto
@main.route('/admin/add-moto', methods=['GET', 'POST'])
@login_required
def add_moto():
    form = AddMotoForm()
    if form.validate_on_submit():
        file = form.image.data
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(current_app.static_folder, 'img', filename)
                file.save(filepath)

                # Redimensionner l'image si besoin (avec PIL)
                with Image.open(filepath) as img:
                    if img.size[0] > 1200 or img.size[1] > 1200:
                        output_size = (1200, 1200)
                        img.thumbnail(output_size)
                        img.save(filepath)

                image_url = filename

                moto = Moto(
                    marque=form.marque.data,
                    modele=form.modele.data,
                    annee=form.annee.data,
                    kilometrage=form.kilometrage.data,
                    prix=float(form.prix.data),
                    description=form.description.data,
                    image_url=image_url
                )
                db.session.add(moto)
                db.session.commit()
                flash('Moto ajoutée avec succès')
                return redirect(url_for('main.home'))
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                db.session.rollback()
                flash(f'Erreur lors de l\'ajout de la moto: {str(e)}')
                return redirect(request.url)
        else:
            flash('Type de fichier non autorisé')
            return redirect(request.url)
    return render_template('add_moto.html', form=form)