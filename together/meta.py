from flask import Blueprint, render_template, current_app, session, url_for, redirect, \
    flash
import datetime
from flask_login import login_user, login_required
from together.forms import RegisterForm, LoginForm
from together.models import User, db


meta = Blueprint('meta', 'together', template_folder='templates/meta')


@meta.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            current_app.logger.warning('Invalid login by "{}".'.format(form.email.data))
            flash('Email/Password mismatching.', 'danger')
            return redirect(url_for('.login'))
        if not login_user(user):
            current_app.logger.warning('Error logging in "{}".'.format(user.email))
            flash('We could not log you in.', 'danger')
            return redirect(url_for('.login'))
        flash('Welcome back {}!'.format(user.name))
        return redirect(url_for('.login'))

    return render_template('login.html')


@meta.route('logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('.login'))

@meta.route('register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.update_password(form.password.data)
        user.active = True
        user.created_at = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('New user "{}" registered with email "{}".'.format(user.name, user.email))
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@meta.route('', defaults={'path': ''})
@meta.route('<path:path>')
@login_required
def angular_view(path):
    return render_template('application.html')
