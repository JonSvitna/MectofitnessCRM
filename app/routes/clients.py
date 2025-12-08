"""Client management routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.client import Client
from datetime import datetime

bp = Blueprint('clients', __name__, url_prefix='/clients')


@bp.route('/')
@login_required
def list_clients():
    """List all clients."""
    page = request.args.get('page', 1, type=int)
    clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).order_by(Client.last_name, Client.first_name).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('clients/list.html', clients=clients)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_client():
    """Add new client."""
    if request.method == 'POST':
        client = Client(
            trainer_id=current_user.id,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            fitness_goal=request.form.get('fitness_goal'),
            fitness_level=request.form.get('fitness_level'),
            medical_conditions=request.form.get('medical_conditions'),
            notes=request.form.get('notes')
        )
        
        db.session.add(client)
        db.session.commit()
        
        flash(f'Client {client.full_name} added successfully!', 'success')
        return redirect(url_for('clients.view_client', client_id=client.id))
    
    return render_template('clients/add.html')


@bp.route('/<int:client_id>')
@login_required
def view_client(client_id):
    """View client details."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    
    # Get client's sessions and programs
    sessions = client.sessions.order_by(Session.scheduled_start.desc()).limit(10).all()
    programs = client.programs.order_by(Program.created_at.desc()).all()
    
    return render_template('clients/view.html', client=client, sessions=sessions, programs=programs)


@bp.route('/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    """Edit client details."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        client.first_name = request.form.get('first_name')
        client.last_name = request.form.get('last_name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.fitness_goal = request.form.get('fitness_goal')
        client.fitness_level = request.form.get('fitness_level')
        client.medical_conditions = request.form.get('medical_conditions')
        client.notes = request.form.get('notes')
        client.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Client {client.full_name} updated successfully!', 'success')
        return redirect(url_for('clients.view_client', client_id=client.id))
    
    return render_template('clients/edit.html', client=client)


@bp.route('/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    """Soft delete client."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    client.is_active = False
    client.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'Client {client.full_name} deleted successfully!', 'success')
    return redirect(url_for('clients.list_clients'))
