from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__)

# User registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration (stub for now)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

# User login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login (stub for now)
        return redirect(url_for('home'))
    return render_template('login.html')
