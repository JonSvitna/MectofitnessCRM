"""API routes for Zoom video conference integration."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.integrations import Integration, VideoConference
from app.models.session import Session
from app.services.zoom_service import zoom_service
from datetime import datetime
import logging

bp = Blueprint('api_zoom', __name__, url_prefix='/api/v1/zoom')
logger = logging.getLogger(__name__)


@bp.route('/status', methods=['GET'])
@login_required
def get_status():
    """Check if Zoom integration is configured and connected."""
    try:
        # Check if integration exists for user
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='zoom'
        ).first()
        
        return jsonify({
            'success': True,
            'configured': zoom_service.is_configured(),
            'connected': integration.is_connected if integration else False,
            'integration_id': integration.id if integration else None
        })
    except Exception as e:
        logger.error(f"Error checking Zoom status: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to check status'}), 500


@bp.route('/connect', methods=['POST'])
@login_required
def connect():
    """Connect Zoom integration for the current user."""
    try:
        data = request.get_json()
        
        # Check if Zoom service is configured
        if not zoom_service.is_configured():
            return jsonify({
                'success': False,
                'error': 'Zoom credentials not configured in server'
            }), 400
        
        # Check if integration already exists
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='zoom'
        ).first()
        
        if not integration:
            integration = Integration(
                trainer_id=current_user.id,
                integration_type='zoom',
                integration_name='Zoom Video Conferencing'
            )
            db.session.add(integration)
        
        # Mark as connected
        integration.is_connected = True
        integration.is_active = True
        integration.last_sync_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Zoom integration connected for user {current_user.id}")
        
        return jsonify({
            'success': True,
            'message': 'Zoom integration connected successfully',
            'integration_id': integration.id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error connecting Zoom: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to connect Zoom'}), 500


@bp.route('/disconnect', methods=['POST'])
@login_required
def disconnect():
    """Disconnect Zoom integration."""
    try:
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='zoom'
        ).first()
        
        if integration:
            integration.is_connected = False
            integration.is_active = False
            db.session.commit()
            
            logger.info(f"Zoom integration disconnected for user {current_user.id}")
        
        return jsonify({
            'success': True,
            'message': 'Zoom integration disconnected'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error disconnecting Zoom: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to disconnect Zoom'}), 500


@bp.route('/meetings', methods=['POST'])
@login_required
def create_meeting():
    """Create a Zoom meeting for a session."""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'success': False, 'error': 'Session ID required'}), 400
        
        # Get the session
        session = Session.query.get(session_id)
        if not session or session.trainer_id != current_user.id:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Check if meeting already exists
        existing_meeting = VideoConference.query.filter_by(session_id=session_id).first()
        if existing_meeting:
            return jsonify({
                'success': False,
                'error': 'Meeting already exists for this session'
            }), 400
        
        # Create meeting via Zoom API
        meeting_info = zoom_service.create_meeting(
            topic=f"Training Session with {session.client.first_name} {session.client.last_name}",
            start_time=session.scheduled_time,
            duration=session.duration or 60,
            agenda=session.notes or "Personal training session"
        )
        
        if not meeting_info:
            return jsonify({
                'success': False,
                'error': 'Failed to create Zoom meeting'
            }), 500
        
        # Save to database
        video_conference = VideoConference(
            session_id=session_id,
            trainer_id=current_user.id,
            platform='zoom',
            meeting_id=meeting_info['meeting_id'],
            meeting_url=meeting_info['meeting_url'],
            meeting_password=meeting_info.get('meeting_password'),
            zoom_meeting_id=meeting_info['meeting_id'],
            status='scheduled',
            scheduled_start=session.scheduled_time
        )
        
        db.session.add(video_conference)
        db.session.commit()
        
        logger.info(f"Zoom meeting created for session {session_id}")
        
        return jsonify({
            'success': True,
            'meeting': {
                'id': video_conference.id,
                'meeting_url': video_conference.meeting_url,
                'meeting_password': video_conference.meeting_password,
                'platform': 'zoom'
            }
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating Zoom meeting: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create meeting'}), 500


@bp.route('/meetings/<int:meeting_id>', methods=['DELETE'])
@login_required
def delete_meeting(meeting_id):
    """Delete a Zoom meeting."""
    try:
        video_conference = VideoConference.query.get(meeting_id)
        
        if not video_conference or video_conference.trainer_id != current_user.id:
            return jsonify({'success': False, 'error': 'Meeting not found'}), 404
        
        # Delete from Zoom
        if video_conference.zoom_meeting_id:
            zoom_service.delete_meeting(video_conference.zoom_meeting_id)
        
        # Delete from database
        db.session.delete(video_conference)
        db.session.commit()
        
        logger.info(f"Zoom meeting {meeting_id} deleted")
        
        return jsonify({
            'success': True,
            'message': 'Meeting deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting Zoom meeting: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete meeting'}), 500


@bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Zoom webhooks."""
    try:
        # Verify webhook (implement proper verification in production)
        data = request.get_json()
        
        event_type = data.get('event')
        payload = data.get('payload', {})
        
        logger.info(f"Received Zoom webhook: {event_type}")
        
        # Handle different event types
        if event_type == 'meeting.started':
            meeting_id = str(payload.get('object', {}).get('id'))
            video_conference = VideoConference.query.filter_by(
                zoom_meeting_id=meeting_id
            ).first()
            
            if video_conference:
                video_conference.status = 'started'
                video_conference.actual_start = datetime.utcnow()
                db.session.commit()
        
        elif event_type == 'meeting.ended':
            meeting_id = str(payload.get('object', {}).get('id'))
            video_conference = VideoConference.query.filter_by(
                zoom_meeting_id=meeting_id
            ).first()
            
            if video_conference:
                video_conference.status = 'ended'
                video_conference.actual_end = datetime.utcnow()
                db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error processing Zoom webhook: {str(e)}")
        return jsonify({'success': False}), 500
