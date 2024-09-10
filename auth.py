from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Registration Form Data:", request.form)  # Debug print
        username = request.form.get('username')
        password = request.form.get('password')
        ethereum_address = request.form.get('ethereum_address')
        
        print(f"Registering: Username: {username}, Ethereum Address: {ethereum_address}")  # Debug print
        
        # In a real application, you'd want to store this information securely
        # For this example, we'll just use session
        session['username'] = username
        session['user_address'] = ethereum_address
        
        print(f"Session after registration: {session}")  # Debug print
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Form Data:", request.form)  # Debug print
        username = request.form.get('username')
        ethereum_address = request.form.get('ethereum_address')
        
        print(f"Username: {username}, Ethereum Address: {ethereum_address}")  # Debug print
        print(f"Session username: {session.get('username')}")  # Debug print
        print(f"Session ethereum_address: {session.get('user_address')}")  # Debug print
        
        if not username or not ethereum_address:
            flash('Both username and Ethereum address are required.', 'error')
            return render_template('login.html'), 400
        
        if username == session.get('username') and ethereum_address == session.get('user_address'):
            print("Username and Ethereum address matched")
            session['logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('marketplace.index'))
        
        flash('Invalid username or Ethereum address', 'error')
        print("Login failed")  # Debug print
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('marketplace.index'))