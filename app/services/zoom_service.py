"""Zoom Integration Service for Video Conferencing."""
import os
import requests
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ZoomService:
    """Service for managing Zoom video conferences."""
    
    def __init__(self):
        """Initialize Zoom service with credentials from environment."""
        self.client_id = os.environ.get('ZOOM_CLIENT_ID')
        self.client_secret = os.environ.get('ZOOM_CLIENT_SECRET')
        self.account_id = os.environ.get('ZOOM_ACCOUNT_ID')
        self.base_url = 'https://api.zoom.us/v2'
        self.oauth_url = 'https://zoom.us/oauth/token'
        self._access_token = None
        self._token_expires_at = None
    
    def is_configured(self) -> bool:
        """Check if Zoom credentials are configured."""
        return all([self.client_id, self.client_secret, self.account_id])
    
    def _get_access_token(self) -> Optional[str]:
        """Get or refresh access token."""
        # Check if we have a valid token
        if self._access_token and self._token_expires_at:
            if datetime.utcnow() < self._token_expires_at:
                return self._access_token
        
        if not self.is_configured():
            logger.error("Zoom credentials not configured")
            return None
        
        try:
            # Create Server-to-Server OAuth token
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('utf-8')
            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'account_credentials',
                'account_id': self.account_id
            }
            
            response = requests.post(self.oauth_url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            self._token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in - 300)  # 5 min buffer
            
            return self._access_token
            
        except Exception as e:
            logger.error(f"Failed to get Zoom access token: {str(e)}")
            return None
    
    def create_meeting(
        self,
        topic: str,
        start_time: datetime,
        duration: int = 60,
        timezone: str = 'UTC',
        password: Optional[str] = None,
        agenda: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Zoom meeting.
        
        Args:
            topic: Meeting topic/title
            start_time: Meeting start time (datetime object)
            duration: Meeting duration in minutes (default: 60)
            timezone: Timezone for the meeting (default: UTC)
            password: Optional meeting password
            agenda: Optional meeting agenda/description
            
        Returns:
            Dictionary with meeting details or None if failed
        """
        token = self._get_access_token()
        if not token:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            meeting_data = {
                'topic': topic,
                'type': 2,  # Scheduled meeting
                'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'duration': duration,
                'timezone': timezone,
                'settings': {
                    'host_video': True,
                    'participant_video': True,
                    'join_before_host': False,
                    'mute_upon_entry': True,
                    'waiting_room': True,
                    'audio': 'both',
                    'auto_recording': 'cloud'  # Auto-record to cloud
                }
            }
            
            if password:
                meeting_data['password'] = password
            
            if agenda:
                meeting_data['agenda'] = agenda
            
            # Use 'me' as user_id for account-level app
            response = requests.post(
                f'{self.base_url}/users/me/meetings',
                headers=headers,
                json=meeting_data
            )
            response.raise_for_status()
            
            meeting_info = response.json()
            
            return {
                'meeting_id': str(meeting_info['id']),
                'meeting_url': meeting_info['join_url'],
                'meeting_password': meeting_info.get('password'),
                'host_url': meeting_info.get('start_url'),
                'platform': 'zoom'
            }
            
        except Exception as e:
            logger.error(f"Failed to create Zoom meeting: {str(e)}")
            return None
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """
        Delete a Zoom meeting.
        
        Args:
            meeting_id: Zoom meeting ID
            
        Returns:
            True if successful, False otherwise
        """
        token = self._get_access_token()
        if not token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.delete(
                f'{self.base_url}/meetings/{meeting_id}',
                headers=headers
            )
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete Zoom meeting: {str(e)}")
            return False
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a Zoom meeting.
        
        Args:
            meeting_id: Zoom meeting ID
            
        Returns:
            Dictionary with meeting details or None if failed
        """
        token = self._get_access_token()
        if not token:
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.get(
                f'{self.base_url}/meetings/{meeting_id}',
                headers=headers
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get Zoom meeting: {str(e)}")
            return None
    
    def update_meeting(
        self,
        meeting_id: str,
        topic: Optional[str] = None,
        start_time: Optional[datetime] = None,
        duration: Optional[int] = None,
        agenda: Optional[str] = None
    ) -> bool:
        """
        Update a Zoom meeting.
        
        Args:
            meeting_id: Zoom meeting ID
            topic: Optional new meeting topic
            start_time: Optional new start time
            duration: Optional new duration in minutes
            agenda: Optional new agenda
            
        Returns:
            True if successful, False otherwise
        """
        token = self._get_access_token()
        if not token:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            update_data = {}
            if topic:
                update_data['topic'] = topic
            if start_time:
                update_data['start_time'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')
            if duration:
                update_data['duration'] = duration
            if agenda:
                update_data['agenda'] = agenda
            
            if not update_data:
                return True  # Nothing to update
            
            response = requests.patch(
                f'{self.base_url}/meetings/{meeting_id}',
                headers=headers,
                json=update_data
            )
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update Zoom meeting: {str(e)}")
            return False


# Singleton instance
zoom_service = ZoomService()
