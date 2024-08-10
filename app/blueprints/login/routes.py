from app.helpers import generate_nonce
from app.forms import Login
from app.models import User, db
from flask import render_template, flash, redirect,url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from . import login

#Object to limit login attempts
limiter = Limiter(get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )


@login.route('/login', methods=['GET', 'POST'])
@limiter.limit("100000 per day",error_message="Lo sentimos, has excedido el limite de intentos para iniciar sesion. Intente mas tarde")
def log_in():
    form = Login()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        try:
            user = User.query.filter_by(username=name).first()
        except SQLAlchemyError as e:
            flash(f'Error en la base de datos: {e}')
            return redirect(url_for('main.index'))
        #checks if user and password matches
        if user and user.validate_password(password):
            login_user(user)
            flash('Has iniciado sesion','success')
            return redirect(url_for('main.index'))
        #if user is None or username or password do not match flash an error
        else:
            flash('Credenciales Incorrectas','warning')
    return render_template('login.html', form=form)

@login.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('main.index'))