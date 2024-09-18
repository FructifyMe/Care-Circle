from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Patient, CareEvent, Note
from app.forms import LoginForm, RegistrationForm, CareEventForm, NoteForm
from app.utils import admin_required
from datetime import datetime

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    patient = Patient.query.first()
    if patient is None:
        # Create a default patient if none exists
        patient = Patient(name="Default Patient", age=0)
        db.session.add(patient)
        db.session.commit()
    care_events = CareEvent.query.filter_by(patient_id=patient.id).all()
    notes = Note.query.filter_by(patient_id=patient.id).order_by(Note.timestamp.desc()).all()
    care_event_form = CareEventForm()
    note_form = NoteForm()
    return render_template('dashboard.html', patient=patient, care_events=care_events, notes=notes, care_event_form=care_event_form, note_form=note_form)

@main.route('/add_care_event', methods=['POST'])
@login_required
def add_care_event():
    form = CareEventForm()
    if form.validate_on_submit():
        patient = Patient.query.first()
        care_event = CareEvent(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            patient_id=patient.id
        )
        db.session.add(care_event)
        db.session.commit()
        flash('Care event added successfully', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/add_note', methods=['POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        patient = Patient.query.first()
        note = Note(
            content=form.content.data,
            patient_id=patient.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully', 'success')
    return redirect(url_for('main.dashboard'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@admin.route('/user_management')
@login_required
@admin_required
def user_management():
    users = User.query.all()
    return render_template('user_management.html', users=users)

@admin.route('/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    else:
        flash('Cannot delete admin users', 'danger')
    return redirect(url_for('admin.user_management'))
