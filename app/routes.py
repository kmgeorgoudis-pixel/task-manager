from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from .forms import RegisterForm, LoginForm, TaskForm
from .models import User, Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Το email χρησιμοποιείται ήδη.', 'danger')
            return redirect(url_for('main.register'))
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Εγγραφή επιτυχής! Μπορείς να συνδεθείς.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Σύνδεση επιτυχής!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Λάθος email ή κωδικός.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Αποσυνδέθηκες με επιτυχία.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data,
            completed=form.completed.data,
            file=filename,
            owner=current_user
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Η εργασία προστέθηκε!', 'success')
        return redirect(url_for('main.dashboard'))

    tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('dashboard.html', form=form, tasks=tasks)

@main.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('Δεν έχεις δικαίωμα να επεξεργαστείς αυτή την εργασία.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        task.completed = form.completed.data

        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            task.file = filename

        db.session.commit()
        flash('Η εργασία ενημερώθηκε!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_task.html', form=form, task=task)

@main.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)