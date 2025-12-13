"""RESTful API for in-app messaging."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from app import db
from app.models.messaging import Message, MessageNotification
from app.models.client import Client
from app.models.user import User

api_messaging = Blueprint('api_messaging', __name__, url_prefix='/api/v1/messages')

def error_response(message, status_code=400, errors=None):
    response = {'success': False, 'error': message}
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

def message_to_dict(message):
    """Convert Message model to dictionary."""
    return {
        'id': message.id,
        'sender_id': message.sender_id,
        'sender_name': message.sender.first_name + ' ' + message.sender.last_name if message.sender else 'Unknown',
        'recipient_type': message.recipient_type,
        'recipient_id': message.recipient_id,
        'subject': message.subject,
        'content': message.content,
        'message_type': message.message_type,
        'attachment_url': message.attachment_url,
        'thread_id': message.thread_id,
        'parent_message_id': message.parent_message_id,
        'is_read': message.is_read,
        'read_at': message.read_at.isoformat() if message.read_at else None,
        'is_archived': message.is_archived,
        'sent_at': message.sent_at.isoformat() if message.sent_at else None,
        'reply_count': len(message.replies) if message.replies else 0,
    }


@api_messaging.route('', methods=['GET'])
@login_required
def get_messages():
    """
    Get messages for the current user.
    
    Query Parameters:
        - thread_id: Filter by thread ID
        - unread_only: Show only unread messages (true/false)
        - archived: Show archived messages (true/false)
        - limit: Limit number of results (default: 50)
    """
    try:
        thread_id = request.args.get('thread_id')
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        archived = request.args.get('archived', 'false').lower() == 'true'
        limit = min(int(request.args.get('limit', 50)), 100)
        
        # Build query - messages where user is sender or recipient
        query = Message.query.filter(
            Message.is_deleted == False
        )
        
        # Filter by thread if specified
        if thread_id:
            query = query.filter(Message.thread_id == thread_id)
        
        # Filter by read status
        if unread_only:
            query = query.filter(Message.is_read == False)
        
        # Filter by archived status
        if archived:
            query = query.filter(Message.is_archived == True)
        else:
            query = query.filter(Message.is_archived == False)
        
        # Get messages where user is sender or recipient
        # For now, we'll get messages where user is sender
        # In a full implementation, you'd also check recipient_id based on recipient_type
        query = query.filter(
            or_(
                Message.sender_id == current_user.id,
                and_(
                    Message.recipient_type == 'trainer',
                    Message.recipient_id == current_user.id
                )
            )
        )
        
        query = query.order_by(Message.sent_at.desc()).limit(limit)
        messages = query.all()
        
        return success_response({
            'messages': [message_to_dict(msg) for msg in messages],
            'count': len(messages)
        })
    except Exception as e:
        return error_response(f'Error fetching messages: {str(e)}', 500)


@api_messaging.route('', methods=['POST'])
@login_required
def create_message():
    """Create a new message."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        recipient_type = data.get('recipient_type', 'client')
        recipient_id = data.get('recipient_id')
        content = data.get('content')
        
        if not recipient_id or not content:
            return error_response('recipient_id and content are required', 400)
        
        # Generate thread_id if not provided
        thread_id = data.get('thread_id')
        if not thread_id:
            thread_id = f"{current_user.id}_{recipient_id}_{datetime.utcnow().timestamp()}"
        
        message = Message(
            sender_id=current_user.id,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            subject=data.get('subject'),
            content=content,
            message_type=data.get('message_type', 'text'),
            attachment_url=data.get('attachment_url'),
            thread_id=thread_id,
            parent_message_id=data.get('parent_message_id'),
        )
        
        db.session.add(message)
        db.session.commit()
        
        return success_response(message_to_dict(message), 'Message sent successfully', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating message: {str(e)}', 500)


@api_messaging.route('/<int:message_id>', methods=['GET'])
@login_required
def get_message(message_id):
    """Get a specific message by ID."""
    try:
        message = Message.query.filter_by(
            id=message_id,
            is_deleted=False
        ).first_or_404()
        
        # Check if user has access to this message
        if message.sender_id != current_user.id and not (
            message.recipient_type == 'trainer' and message.recipient_id == current_user.id
        ):
            return error_response('Access denied', 403)
        
        return success_response(message_to_dict(message))
    except Exception as e:
        return error_response(f'Error fetching message: {str(e)}', 500)


@api_messaging.route('/<int:message_id>/read', methods=['POST'])
@login_required
def mark_as_read(message_id):
    """Mark a message as read."""
    try:
        message = Message.query.filter_by(
            id=message_id,
            is_deleted=False
        ).first_or_404()
        
        # Check if user has access
        if message.recipient_type == 'trainer' and message.recipient_id == current_user.id:
            message.mark_as_read()
            db.session.commit()
            return success_response(message_to_dict(message), 'Message marked as read')
        
        return error_response('Access denied', 403)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error marking message as read: {str(e)}', 500)


@api_messaging.route('/<int:message_id>/archive', methods=['POST'])
@login_required
def archive_message(message_id):
    """Archive or unarchive a message."""
    try:
        message = Message.query.filter_by(
            id=message_id,
            is_deleted=False
        ).first_or_404()
        
        # Check if user has access
        if message.sender_id != current_user.id and not (
            message.recipient_type == 'trainer' and message.recipient_id == current_user.id
        ):
            return error_response('Access denied', 403)
        
        data = request.get_json() or {}
        archive = data.get('archive', True)
        
        message.is_archived = archive
        db.session.commit()
        
        return success_response(message_to_dict(message), f'Message {"archived" if archive else "unarchived"}')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error archiving message: {str(e)}', 500)


@api_messaging.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get message statistics for the current user."""
    try:
        total = Message.query.filter(
            or_(
                Message.sender_id == current_user.id,
                and_(
                    Message.recipient_type == 'trainer',
                    Message.recipient_id == current_user.id
                )
            ),
            Message.is_deleted == False
        ).count()
        
        unread = Message.query.filter(
            and_(
                Message.recipient_type == 'trainer',
                Message.recipient_id == current_user.id,
                Message.is_read == False,
                Message.is_deleted == False
            )
        ).count()
        
        return success_response({
            'total': total,
            'unread': unread,
            'archived': Message.query.filter(
                or_(
                    Message.sender_id == current_user.id,
                    and_(
                        Message.recipient_type == 'trainer',
                        Message.recipient_id == current_user.id
                    )
                ),
                Message.is_deleted == False,
                Message.is_archived == True
            ).count()
        })
    except Exception as e:
        return error_response(f'Error fetching stats: {str(e)}', 500)

