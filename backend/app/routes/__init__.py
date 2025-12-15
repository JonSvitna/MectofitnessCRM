"""API routes for MectoFitness Backend."""
from flask import Blueprint, request, jsonify
from app import db
from app.models import Lead
from email_validator import validate_email, EmailNotValidError
import logging

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@api_bp.route('/leads', methods=['POST'])
def create_lead():
    """Create a new lead from landing page signup."""
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'business_type']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        # Validate email format
        try:
            email_info = validate_email(data['email'], check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            return jsonify({'error': f'Invalid email: {str(e)}'}), 400
        
        # Check if email already exists
        existing_lead = Lead.query.filter_by(email=email).first()
        if existing_lead:
            return jsonify({
                'error': 'Email already registered',
                'message': 'This email address is already in our system.'
            }), 409
        
        # Create new lead
        lead = Lead(
            name=data['name'].strip(),
            email=email,
            phone=data.get('phone', '').strip() or None,
            business_type=data['business_type'],
            message=data.get('message', '').strip() or None,
            source=data.get('source', 'landing_page'),
            status='new'
        )
        
        # Save to database
        db.session.add(lead)
        db.session.commit()
        
        logger.info(f"New lead created: {lead.email}")
        
        return jsonify({
            'message': 'Lead created successfully',
            'lead': lead.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating lead: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to create lead. Please try again.'
        }), 500


@api_bp.route('/leads', methods=['GET'])
def get_leads():
    """Get all leads (for admin/CRM access)."""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page
        
        # Filter by status
        status = request.args.get('status')
        
        # Query
        query = Lead.query
        if status:
            query = query.filter_by(status=status)
        
        # Order by created_at desc
        query = query.order_by(Lead.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'leads': [lead.to_dict() for lead in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching leads: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to fetch leads.'
        }), 500


@api_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead by ID."""
    try:
        lead = Lead.query.get_or_404(lead_id)
        return jsonify(lead.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching lead {lead_id}: {str(e)}")
        return jsonify({
            'error': 'Lead not found'
        }), 404


@api_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead (e.g., change status)."""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            lead.status = data['status']
        if 'message' in data:
            lead.message = data['message']
        
        db.session.commit()
        
        logger.info(f"Lead updated: {lead.email}")
        
        return jsonify({
            'message': 'Lead updated successfully',
            'lead': lead.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating lead {lead_id}: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to update lead.'
        }), 500


@api_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead."""
    try:
        lead = Lead.query.get_or_404(lead_id)
        db.session.delete(lead)
        db.session.commit()
        
        logger.info(f"Lead deleted: {lead.email}")
        
        return jsonify({'message': 'Lead deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting lead {lead_id}: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to delete lead.'
        }), 500
