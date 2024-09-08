from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            ethereum_address = request.form['ethereum_address']
            bio = request.form.get('bio', '')  # Bio is optional
            
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.', 'error')
                return redirect(url_for('auth.register'))
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', 'error')
                return redirect(url_for('auth.register'))
            
            new_user = User(username=username, email=email, ethereum_address=ethereum_address, bio=bio)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            print(f"Registration error: {str(e)}")  # For server-side logging
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_address'] = user.ethereum_address
            flash('Logged in successfully.', 'success')
            return redirect(url_for('marketplace.index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_address', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('marketplace.index'))

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to edit your profile.', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.bio = request.form['bio']
        user.ethereum_address = request.form['ethereum_address']
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('edit_profile.html', user=user)