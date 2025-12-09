"""Authentication routes."""
import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Use the new authenticate method with better error handling
        user, error = User.authenticate(username, password)
        
        if user:
            try:
                login_user(user, remember=remember)
                logger.info(f"User logged in: {user.username}")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.dashboard'))
            except Exception as e:
                logger.error(f"Login failed for user {username}: {str(e)}")
                flash('Login failed. Please try again.', 'danger')
        else:
            logger.warning(f"Failed login attempt for: {username}")
            flash(error or 'Invalid username or password', 'danger')
    
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            
            # Use the new create_user method with better error handling
            user, error = User.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            if user:
                logger.info(f"New user registered: {username}")
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                logger.warning(f"Registration failed for {username}: {error}")
                # Don't expose sensitive error details to users
                flash(error or 'Registration failed. Please try again.', 'danger')
                return redirect(url_for('auth.register'))
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            # Don't expose sensitive error details to users
            flash('Registration failed. Please try again or contact support if the problem persists.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')


@bp.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
