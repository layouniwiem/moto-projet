# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Moto
from .forms import LoginForm
from . import db

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))