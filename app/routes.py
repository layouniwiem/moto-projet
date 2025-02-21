import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Moto
from .forms import LoginForm
from . import db
from werkzeug.utils import secure_filename
from PIL import Image 

# Configuration pour l'upload des fichiers
UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite à 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

main = Blueprint('main', __name__,static_folder='static', template_folder='templates')
auth = Blueprint('auth', __name__,static_folder='static', template_folder='templates')
# Dans routes.py
@main.route('/')
def home():
    motos = Moto.query.order_by(Moto.date_ajout.desc()).all()
    return render_template('home.html', motos=motos)

@main.route('/moto/<int:id>')
def moto_details(id):
    moto = Moto.query.get_or_404(id)
    return render_template('moto_details.html', moto=moto)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('authenticated')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            print('authenticated')
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        flash('Nom d\'utilisateur ou mot de passe incorrect')
    print('not authenticated')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/admin/add-moto', methods=['GET', 'POST'])
@login_required
def add_moto():
    if request.method == 'POST':
        # Vérifier si le formulaire contient un fichier
        if 'image' not in request.files:
            flash('Aucune image sélectionnée')
            return redirect(request.url)
            
        file = request.files['image']
        
        # Si l'utilisateur n'a pas sélectionné de fichier
        if file.filename == '':
            flash('Aucune image sélectionnée')
            return redirect(request.url)

        # Vérifier si le fichier est autorisé et le sauvegarder
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                # Créer le dossier s'il n'existe pas
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    

                filepath = os.path.join(current_app.static_folder, 'img', filename)
                file.save(filepath)
                
                # Vérifier et redimensionner l'image si nécessaire
                with Image.open(filepath) as img:
                    if img.size[0] > 1200 or img.size[1] > 1200:
                        output_size = (1200, 1200)
                        img.thumbnail(output_size)
                        img.save(filepath)

                image_url = f'/static/img/{filename}'
                
                # Créer la moto avec l'image
                moto = Moto(
                    marque=request.form['marque'],
                    modele=request.form['modele'],
                    annee=int(request.form['annee']),
                    kilometrage=int(request.form['kilometrage']),
                    prix=float(request.form['prix']),
                    description=request.form['description'],
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
            
    return render_template('add_moto.html')