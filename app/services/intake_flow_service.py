"""Client intake workflow service with email and document automation."""
import os
from typing import Dict, List, Optional
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import db
from app.models.client import Client


class IntakeFlowService:
    """
    Service for managing automated client intake workflows.
    Handles email sending, document management, and progress tracking.
    """
    
    def __init__(self):
        """Initialize the intake flow service."""
        self.sendgrid_key = os.environ.get('SENDGRID_API_KEY')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@mectofitness.com')
        self.twilio_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    def is_email_configured(self) -> bool:
        """Check if email service is configured."""
        return bool(self.sendgrid_key)
    
    def is_sms_configured(self) -> bool:
        """Check if SMS service is configured."""
        return bool(self.twilio_sid and self.twilio_token)
    
    def send_welcome_email(
        self,
        client_id: int,
        trainer_name: str,
        custom_message: Optional[str] = None
    ) -> Dict:
        """
        Send welcome email to new client.
        
        Args:
            client_id: Client ID
            trainer_name: Name of the trainer
            custom_message: Optional custom message to include
            
        Returns:
            Dictionary with success status and message
        """
        try:
            client = Client.query.get(client_id)
            if not client:
                return {"success": False, "error": "Client not found"}
            
            if not self.is_email_configured():
                return {"success": False, "error": "SendGrid not configured"}
            
            # Build email content
            subject = f"Welcome to {trainer_name}'s Training Program! 🏋️"
            
            html_content = self._get_welcome_email_template(
                client_name=client.full_name,
                trainer_name=trainer_name,
                custom_message=custom_message
            )
            
            # Send via SendGrid
            message = Mail(
                from_email=self.from_email,
                to_emails=client.email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            return {
                "success": True,
                "message": "Welcome email sent successfully",
                "status_code": response.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send welcome email"
            }
    
    def send_intake_form_request(
        self,
        client_id: int,
        trainer_name: str,
        intake_form_url: str
    ) -> Dict:
        """Send intake form completion request."""
        try:
            client = Client.query.get(client_id)
            if not client or not self.is_email_configured():
                return {"success": False, "error": "Client not found or email not configured"}
            
            subject = f"Complete Your Fitness Assessment - {trainer_name}"
            
            html_content = self._get_intake_form_email_template(
                client_name=client.full_name,
                trainer_name=trainer_name,
                form_url=intake_form_url
            )
            
            message = Mail(
                from_email=self.from_email,
                to_emails=client.email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            return {"success": True, "message": "Intake form request sent"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_document_signing_request(
        self,
        client_id: int,
        trainer_name: str,
        document_type: str,
        document_url: str
    ) -> Dict:
        """Send document signing request (waiver, consent, etc.)."""
        try:
            client = Client.query.get(client_id)
            if not client or not self.is_email_configured():
                return {"success": False, "error": "Client not found or email not configured"}
            
            subject = f"Action Required: Sign {document_type} - {trainer_name}"
            
            html_content = self._get_document_signing_email_template(
                client_name=client.full_name,
                trainer_name=trainer_name,
                document_type=document_type,
                document_url=document_url
            )
            
            message = Mail(
                from_email=self.from_email,
                to_emails=client.email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            return {"success": True, "message": "Document signing request sent"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_photo_upload_request(
        self,
        client_id: int,
        trainer_name: str,
        upload_url: str
    ) -> Dict:
        """Send progress photo upload request."""
        try:
            client = Client.query.get(client_id)
            if not client or not self.is_email_configured():
                return {"success": False, "error": "Client not found or email not configured"}
            
            subject = f"Upload Your Progress Photos - {trainer_name}"
            
            html_content = self._get_photo_upload_email_template(
                client_name=client.full_name,
                trainer_name=trainer_name,
                upload_url=upload_url
            )
            
            message = Mail(
                from_email=self.from_email,
                to_emails=client.email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            return {"success": True, "message": "Photo upload request sent"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_welcome_email_template(
        self,
        client_name: str,
        trainer_name: str,
        custom_message: Optional[str] = None
    ) -> str:
        """Get HTML template for welcome email."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 12px 24px; background: #FF6B35; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
        h1 {{ margin: 0; font-size: 28px; }}
        h2 {{ color: #FF6B35; font-size: 22px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏋️ Welcome to Your Fitness Journey!</h1>
        </div>
        <div class="content">
            <p>Hi {client_name},</p>
            
            <p>Welcome! I'm excited to be your trainer and help you achieve your fitness goals.</p>
            
            {f'<p style="background: #f8f9fa; padding: 15px; border-left: 4px solid #FF6B35; margin: 20px 0;"><strong>Message from {trainer_name}:</strong><br>{custom_message}</p>' if custom_message else ''}
            
            <h2>What's Next?</h2>
            <p>To get started, please complete these steps:</p>
            <ul>
                <li><strong>Complete your intake form</strong> - Help me understand your goals and fitness history</li>
                <li><strong>Sign required documents</strong> - Liability waiver and training agreement</li>
                <li><strong>Submit progress photos</strong> - Before photos to track your transformation</li>
                <li><strong>Schedule your first session</strong> - Let's get you started!</li>
            </ul>
            
            <p>You'll receive separate emails with links for each of these steps.</p>
            
            <h2>What to Expect</h2>
            <ul>
                <li>Personalized training programs designed for your goals</li>
                <li>Regular progress tracking and adjustments</li>
                <li>Professional guidance and support</li>
                <li>Access to 722+ professional exercises</li>
            </ul>
            
            <p>If you have any questions, feel free to reach out anytime!</p>
            
            <p>Let's make this happen! 💪</p>
            
            <p>Best regards,<br><strong>{trainer_name}</strong></p>
        </div>
        <div class="footer">
            <p>MectoFitness CRM - Professional Personal Training Software</p>
            <p style="font-size: 12px;">This email was sent because you were added as a client. If you believe this was sent in error, please contact your trainer.</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_intake_form_email_template(
        self,
        client_name: str,
        trainer_name: str,
        form_url: str
    ) -> str:
        """Get HTML template for intake form request."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #004E89 0%, #1AE5BE 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 14px 28px; background: #FF6B35; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
        h1 {{ margin: 0; font-size: 28px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Complete Your Fitness Assessment</h1>
        </div>
        <div class="content">
            <p>Hi {client_name},</p>
            
            <p>To create the perfect training program for you, I need to learn more about your fitness goals, experience, and current health status.</p>
            
            <p>Please take 5-10 minutes to complete your intake form. This information will help me design a program that's safe, effective, and tailored specifically to you.</p>
            
            <p style="text-align: center;">
                <a href="{form_url}" class="button">Complete Intake Form →</a>
            </p>
            
            <p><strong>What's Included:</strong></p>
            <ul>
                <li>Your fitness goals and timeline</li>
                <li>Current activity level and experience</li>
                <li>Health history and any limitations</li>
                <li>Exercise preferences and equipment access</li>
                <li>Nutrition and lifestyle information</li>
            </ul>
            
            <p>This information is confidential and will only be used to create your personalized program.</p>
            
            <p>Thank you!<br><strong>{trainer_name}</strong></p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_document_signing_email_template(
        self,
        client_name: str,
        trainer_name: str,
        document_type: str,
        document_url: str
    ) -> str:
        """Get HTML template for document signing request."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 14px 28px; background: #FF6B35; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
        .alert {{ background: #FFF3CD; border-left: 4px solid #FFC107; padding: 15px; margin: 20px 0; }}
        h1 {{ margin: 0; font-size: 28px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✍️ Action Required: Sign Document</h1>
        </div>
        <div class="content">
            <p>Hi {client_name},</p>
            
            <p>Before we begin training, you'll need to review and sign the following document:</p>
            
            <div class="alert">
                <strong>{document_type}</strong>
            </div>
            
            <p>This is a standard requirement for all personal training clients. The document includes important information about:</p>
            <ul>
                <li>Assumption of risk and liability</li>
                <li>Health and safety guidelines</li>
                <li>Terms of service</li>
                <li>Cancellation policies</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="{document_url}" class="button">Review and Sign Document →</a>
            </p>
            
            <p>The process takes just 2-3 minutes. You'll be able to review the full document before signing.</p>
            
            <p>If you have any questions about the document, please don't hesitate to reach out.</p>
            
            <p>Best regards,<br><strong>{trainer_name}</strong></p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_photo_upload_email_template(
        self,
        client_name: str,
        trainer_name: str,
        upload_url: str
    ) -> str:
        """Get HTML template for photo upload request."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1AE5BE 0%, #004E89 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 14px 28px; background: #FF6B35; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 20px 0; }}
        .tip-box {{ background: #E3F2FD; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; }}
        h1 {{ margin: 0; font-size: 28px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📸 Upload Your Progress Photos</h1>
        </div>
        <div class="content">
            <p>Hi {client_name},</p>
            
            <p>Progress photos are one of the best ways to track your transformation! Visual progress often appears before the scale moves, so these photos will be valuable motivation throughout your journey.</p>
            
            <p style="text-align: center;">
                <a href="{upload_url}" class="button">Upload Photos →</a>
            </p>
            
            <p><strong>What Photos to Take:</strong></p>
            <ul>
                <li><strong>Front view</strong> - Standing straight, arms at sides</li>
                <li><strong>Side view</strong> - Profile shot, both left and right</li>
                <li><strong>Back view</strong> - Shoulders and back visible</li>
            </ul>
            
            <div class="tip-box">
                <p><strong>📸 Photo Tips:</strong></p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Take photos in the same location each time</li>
                    <li>Use natural lighting if possible</li>
                    <li>Wear fitted clothing (athletic wear works great)</li>
                    <li>Stand in the same pose for consistency</li>
                    <li>Take photos at the same time of day</li>
                </ul>
            </div>
            
            <p><strong>Privacy:</strong> Your photos are private and secure. Only you and your trainer will have access to them. They will never be shared without your explicit permission.</p>
            
            <p>These photos will help us celebrate your progress together!</p>
            
            <p>Best regards,<br><strong>{trainer_name}</strong></p>
        </div>
    </div>
</body>
</html>
"""


# Default document templates
DEFAULT_LIABILITY_WAIVER = """
<h1>LIABILITY WAIVER AND ASSUMPTION OF RISK</h1>

<p>I, {{CLIENT_NAME}}, hereby acknowledge that I have voluntarily chosen to participate in personal training sessions with {{TRAINER_NAME}}.</p>

<h2>Assumption of Risk</h2>
<p>I understand and acknowledge that:</p>
<ul>
    <li>Physical exercise involves certain inherent risks including, but not limited to, minor injuries (such as bruises, strains), serious injuries (such as joint or back injuries, heart attacks, stroke), and catastrophic injuries (including paralysis and death).</li>
    <li>I voluntarily assume all risks associated with participation in this training program.</li>
    <li>I am in good physical condition and have no medical conditions that would prevent me from participating in physical exercise.</li>
</ul>

<h2>Medical Clearance</h2>
<p>I certify that:</p>
<ul>
    <li>I have consulted with a physician regarding my participation in this exercise program, OR</li>
    <li>I have chosen not to consult with a physician prior to beginning this program</li>
</ul>

<h2>Release of Liability</h2>
<p>I hereby release, waive, and discharge {{TRAINER_NAME}} and any affiliated entities from any and all claims, demands, or causes of action arising from my participation in personal training sessions.</p>

<h2>Emergency Medical Treatment</h2>
<p>I authorize {{TRAINER_NAME}} to obtain emergency medical treatment on my behalf if necessary.</p>

<p><strong>I have read this waiver and fully understand its contents. I voluntarily agree to its terms and conditions.</strong></p>

<p>Client Signature: _______________________</p>
<p>Date: _______________________</p>
"""

DEFAULT_PAR_Q_FORM = """
<h1>PAR-Q & YOU - Physical Activity Readiness Questionnaire</h1>

<p><strong>Client Name:</strong> {{CLIENT_NAME}}</p>

<p>Regular physical activity is fun and healthy, and increasingly more people are starting to become more active every day. Being more active is very safe for most people. However, some people should check with their doctor before they start becoming much more physically active.</p>

<p><strong>Please answer the following questions honestly:</strong></p>

<h2>Medical History</h2>
<ol>
    <li>Has your doctor ever said that you have a heart condition and that you should only do physical activity recommended by a doctor? <strong>YES / NO</strong></li>
    <li>Do you feel pain in your chest when you do physical activity? <strong>YES / NO</strong></li>
    <li>In the past month, have you had chest pain when you were not doing physical activity? <strong>YES / NO</strong></li>
    <li>Do you lose your balance because of dizziness or do you ever lose consciousness? <strong>YES / NO</strong></li>
    <li>Do you have a bone or joint problem that could be made worse by a change in your physical activity? <strong>YES / NO</strong></li>
    <li>Is your doctor currently prescribing drugs for your blood pressure or heart condition? <strong>YES / NO</strong></li>
    <li>Do you know of any other reason why you should not do physical activity? <strong>YES / NO</strong></li>
</ol>

<p><strong>If you answered YES to one or more questions:</strong> Talk with your doctor before you start becoming much more physically active or before you have a fitness appraisal. Tell your doctor about the PAR-Q and which questions you answered YES.</p>

<p><strong>If you answered NO to all questions:</strong> You can be reasonably sure that you can start becoming more physically active and participate in a fitness appraisal.</p>

<h2>Declaration</h2>
<p>I have read, understood and completed this questionnaire. Any questions I had were answered to my full satisfaction.</p>

<p>Client Signature: _______________________</p>
<p>Date: _______________________</p>
"""
