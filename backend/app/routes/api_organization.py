"""RESTful API for organization management."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
import re
from app import db
from app.models.organization import Organization
from app.models.user import User
from app.models.client import Client
from app.utils.rbac import owner_required, admin_required

api_organization = Blueprint('api_organization', __name__, url_prefix='/api/v1/organization')

def error_response(message, status_code=400, errors=None):
    response = {'success': False, 'error': message}
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:100]

@api_organization.route('/', methods=['GET'])
@login_required
def get_organization():
    """Get current user's organization details."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        org = Organization.query.get(current_user.organization_id)
        if not org:
            return error_response('Organization not found', 404)
        
        return success_response({
            'id': org.id,
            'name': org.name,
            'slug': org.slug,
            'business_type': org.business_type,
            'email': org.email,
            'phone': org.phone,
            'website': org.website,
            'address': {
                'line1': org.address_line1,
                'line2': org.address_line2,
                'city': org.city,
                'state': org.state,
                'zip_code': org.zip_code,
                'country': org.country
            },
            'subscription_tier': org.subscription_tier,
            'max_trainers': org.max_trainers,
            'max_clients': org.max_clients,
            'trainer_count': org.trainer_count,
            'client_count': org.client_count,
            'logo_url': org.logo_url,
            'primary_color': org.primary_color,
            'is_active': org.is_active,
            'created_at': org.created_at.isoformat()
        })
    except Exception as e:
        return error_response(f'Error fetching organization: {str(e)}', 500)

@api_organization.route('/', methods=['POST'])
@login_required
def create_organization():
    """Create a new organization (for new owners)."""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return error_response('Organization name is required')
        
        # Check if user already has an organization
        if current_user.organization_id:
            return error_response('User already belongs to an organization', 400)
        
        # Generate slug
        slug = slugify(data['name'])
        counter = 1
        original_slug = slug
        while Organization.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Create organization
        org = Organization(
            name=data['name'],
            slug=slug,
            business_type=data.get('business_type'),
            email=data.get('email', current_user.email),
            phone=data.get('phone'),
            website=data.get('website'),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            country=data.get('country', 'USA'),
            subscription_tier=data.get('subscription_tier', 'free'),
            max_trainers=data.get('max_trainers', 1),
            max_clients=data.get('max_clients', 10)
        )
        db.session.add(org)
        db.session.flush()
        
        # Assign user to organization as owner
        current_user.organization_id = org.id
        current_user.role = 'owner'
        current_user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'id': org.id,
            'name': org.name,
            'slug': org.slug,
            'role': 'owner'
        }, 'Organization created successfully', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating organization: {str(e)}', 500)

@api_organization.route('/', methods=['PUT', 'PATCH'])
@login_required
@owner_required
def update_organization():
    """Update organization details (owner only)."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        org = Organization.query.get(current_user.organization_id)
        if not org:
            return error_response('Organization not found', 404)
        
        data = request.get_json()
        
        # Update basic fields
        fields = ['name', 'business_type', 'email', 'phone', 'website',
                 'address_line1', 'address_line2', 'city', 'state', 
                 'zip_code', 'country', 'logo_url', 'primary_color']
        
        for field in fields:
            if field in data:
                setattr(org, field, data[field])
        
        # Update slug if name changed
        if 'name' in data:
            new_slug = slugify(data['name'])
            if new_slug != org.slug:
                counter = 1
                original_slug = new_slug
                while Organization.query.filter(
                    Organization.slug == new_slug,
                    Organization.id != org.id
                ).first():
                    new_slug = f"{original_slug}-{counter}"
                    counter += 1
                org.slug = new_slug
        
        org.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response({'id': org.id, 'slug': org.slug}, 'Organization updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating organization: {str(e)}', 500)

@api_organization.route('/members', methods=['GET'])
@login_required
@admin_required
def get_organization_members():
    """Get all members in the organization (admin/owner only)."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        members = User.query.filter_by(
            organization_id=current_user.organization_id,
            is_active=True
        ).order_by(User.created_at.desc()).all()
        
        return success_response({'members': [{
            'id': m.id,
            'username': m.username,
            'email': m.email,
            'full_name': m.full_name,
            'role': m.role,
            'specialization': m.specialization,
            'phone': m.phone,
            'is_active': m.is_active,
            'created_at': m.created_at.isoformat()
        } for m in members]})
    except Exception as e:
        return error_response(f'Error fetching members: {str(e)}', 500)

@api_organization.route('/members/<int:user_id>/role', methods=['PATCH'])
@login_required
@owner_required
def update_member_role(user_id):
    """Update member role (owner only)."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        user = User.query.get(user_id)
        if not user or user.organization_id != current_user.organization_id:
            return error_response('User not found in organization', 404)
        
        # Prevent changing own role
        if user.id == current_user.id:
            return error_response('Cannot change your own role', 400)
        
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['owner', 'admin', 'trainer', 'client']:
            return error_response('Invalid role')
        
        # Prevent creating multiple owners
        if new_role == 'owner':
            return error_response('Cannot assign owner role. Transfer ownership instead.', 400)
        
        user.role = new_role
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response({'id': user.id, 'role': new_role}, 'Role updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating role: {str(e)}', 500)

@api_organization.route('/invite', methods=['POST'])
@login_required
@admin_required
def invite_member():
    """Invite new member to organization (admin/owner only)."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        org = Organization.query.get(current_user.organization_id)
        if not org:
            return error_response('Organization not found', 404)
        
        data = request.get_json()
        if not data or not data.get('email') or not data.get('role'):
            return error_response('Email and role are required')
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return error_response('User with this email already exists')
        
        # Check organization limits
        if data['role'] == 'trainer' and org.trainer_count >= org.max_trainers:
            return error_response(f'Trainer limit reached ({org.max_trainers})')
        
        # For now, create user directly (in production, send invitation email)
        username = data['email'].split('@')[0]
        counter = 1
        original_username = username
        while User.query.filter_by(username=username).first():
            username = f"{original_username}{counter}"
            counter += 1
        
        user = User(
            username=username,
            email=data['email'],
            organization_id=current_user.organization_id,
            role=data['role'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone')
        )
        # Set temporary password (should be changed on first login)
        user.set_password(data.get('temporary_password', 'ChangeMe123!'))
        
        db.session.add(user)
        db.session.commit()
        
        return success_response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role
        }, 'Member invited successfully', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error inviting member: {str(e)}', 500)

@api_organization.route('/stats', methods=['GET'])
@login_required
@admin_required
def get_organization_stats():
    """Get organization statistics (admin/owner only)."""
    try:
        if not current_user.organization_id:
            return error_response('No organization assigned', 404)
        
        org = Organization.query.get(current_user.organization_id)
        if not org:
            return error_response('Organization not found', 404)
        
        # Get all trainers in organization
        trainers = User.query.filter_by(
            organization_id=org.id
        ).filter(User.role.in_(['owner', 'admin', 'trainer'])).all()
        
        trainer_ids = [t.id for t in trainers]
        
        # Count total clients across all trainers
        from app.models.session import Session
        from app.models.program import Program
        
        total_clients = Client.query.filter(
            Client.trainer_id.in_(trainer_ids)
        ).count()
        
        active_clients = Client.query.filter(
            Client.trainer_id.in_(trainer_ids),
            Client.status == 'active'
        ).count()
        
        total_sessions = Session.query.filter(
            Session.trainer_id.in_(trainer_ids)
        ).count()
        
        active_programs = Program.query.filter(
            Program.trainer_id.in_(trainer_ids),
            Program.status == 'active'
        ).count()
        
        return success_response({
            'organization': {
                'name': org.name,
                'subscription_tier': org.subscription_tier
            },
            'members': {
                'total_trainers': len(trainers),
                'max_trainers': org.max_trainers
            },
            'clients': {
                'total': total_clients,
                'active': active_clients,
                'max_clients': org.max_clients
            },
            'sessions': {
                'total': total_sessions
            },
            'programs': {
                'active': active_programs
            }
        })
    except Exception as e:
        return error_response(f'Error fetching stats: {str(e)}', 500)
