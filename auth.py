from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ethereum_address = request.form['ethereum_address']
        
        # In a real application, you'd want to store this information securely
        # For this example, we'll just use session
        session['username'] = username
        session['user_address'] = ethereum_address
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        ethereum_address = request.form['ethereum_address']
        
        if username == session.get('username') and ethereum_address == session.get('user_address'):
            session['logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('marketplace.index'))
        flash('Invalid username or Ethereum address', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('marketplace.index'))