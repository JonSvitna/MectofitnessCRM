"""Marketing automation routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.marketing import EmailTemplate, SMSTemplate, MarketingCampaign, CommunicationLog
from app.models.client import Client
from datetime import datetime
import json

bp = Blueprint('marketing', __name__, url_prefix='/marketing')


@bp.route('/')
@login_required
def dashboard():
    """Marketing dashboard."""
    campaigns = MarketingCampaign.query.filter_by(
        trainer_id=current_user.id
    ).order_by(MarketingCampaign.created_at.desc()).limit(5).all()
    
    email_templates = EmailTemplate.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).count()
    
    sms_templates = SMSTemplate.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).count()
    
    return render_template('marketing/dashboard.html',
                         campaigns=campaigns,
                         email_templates=email_templates,
                         sms_templates=sms_templates)


# Email Templates
@bp.route('/email-templates')
@login_required
def list_email_templates():
    """List email templates."""
    templates = EmailTemplate.query.filter_by(
        trainer_id=current_user.id
    ).order_by(EmailTemplate.created_at.desc()).all()
    return render_template('marketing/email_templates.html', templates=templates)


@bp.route('/email-templates/create', methods=['GET', 'POST'])
@login_required
def create_email_template():
    """Create email template."""
    if request.method == 'POST':
        template = EmailTemplate(
            trainer_id=current_user.id,
            name=request.form.get('name'),
            subject=request.form.get('subject'),
            body=request.form.get('body'),
            category=request.form.get('category')
        )
        
        db.session.add(template)
        db.session.commit()
        
        flash('Email template created!', 'success')
        return redirect(url_for('marketing.list_email_templates'))
    
    return render_template('marketing/create_email_template.html')


@bp.route('/email-templates/<int:template_id>/generate-ai', methods=['POST'])
@login_required
def generate_ai_email(template_id=None):
    """Generate AI email template."""
    prompt = request.form.get('prompt')
    category = request.form.get('category')
    
    # AI Generation Logic (placeholder)
    # This would call an AI service like OpenAI to generate email content
    
    ai_subject = f"AI-Generated: {prompt[:50]}"
    ai_body = f"""Dear {{client_name}},

This is an AI-generated email based on your requirements.

Prompt: {prompt}

Best regards,
{{trainer_name}}
"""
    
    template = EmailTemplate(
        trainer_id=current_user.id,
        name=f"AI: {prompt[:30]}",
        subject=ai_subject,
        body=ai_body,
        category=category,
        is_ai_generated=True,
        ai_prompt=prompt
    )
    
    db.session.add(template)
    db.session.commit()
    
    flash('AI email template generated!', 'success')
    return redirect(url_for('marketing.list_email_templates'))


# SMS Templates
@bp.route('/sms-templates')
@login_required
def list_sms_templates():
    """List SMS templates."""
    templates = SMSTemplate.query.filter_by(
        trainer_id=current_user.id
    ).order_by(SMSTemplate.created_at.desc()).all()
    return render_template('marketing/sms_templates.html', templates=templates)


@bp.route('/sms-templates/create', methods=['GET', 'POST'])
@login_required
def create_sms_template():
    """Create SMS template."""
    if request.method == 'POST':
        template = SMSTemplate(
            trainer_id=current_user.id,
            name=request.form.get('name'),
            message=request.form.get('message'),
            category=request.form.get('category')
        )
        
        db.session.add(template)
        db.session.commit()
        
        flash('SMS template created!', 'success')
        return redirect(url_for('marketing.list_sms_templates'))
    
    return render_template('marketing/create_sms_template.html')


@bp.route('/sms-templates/generate-ai', methods=['POST'])
@login_required
def generate_ai_sms():
    """Generate AI SMS template."""
    prompt = request.form.get('prompt')
    category = request.form.get('category')
    
    # AI Generation Logic (placeholder)
    ai_message = f"Hi {{client_name}}! {prompt[:100]}"
    
    template = SMSTemplate(
        trainer_id=current_user.id,
        name=f"AI: {prompt[:30]}",
        message=ai_message,
        category=category,
        is_ai_generated=True,
        ai_prompt=prompt
    )
    
    db.session.add(template)
    db.session.commit()
    
    flash('AI SMS template generated!', 'success')
    return redirect(url_for('marketing.list_sms_templates'))


# Campaigns
@bp.route('/campaigns')
@login_required
def list_campaigns():
    """List marketing campaigns."""
    campaigns = MarketingCampaign.query.filter_by(
        trainer_id=current_user.id
    ).order_by(MarketingCampaign.created_at.desc()).all()
    return render_template('marketing/campaigns.html', campaigns=campaigns)


@bp.route('/campaigns/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    """Create marketing campaign."""
    if request.method == 'POST':
        campaign = MarketingCampaign(
            trainer_id=current_user.id,
            name=request.form.get('name'),
            description=request.form.get('description'),
            campaign_type=request.form.get('campaign_type'),
            target_segment=request.form.get('target_segment'),
            trigger_type=request.form.get('trigger_type'),
            email_template_id=request.form.get('email_template_id', type=int) or None,
            sms_template_id=request.form.get('sms_template_id', type=int) or None,
            status='draft'
        )
        
        # Handle scheduled date
        scheduled_date = request.form.get('scheduled_date')
        if scheduled_date:
            campaign.scheduled_date = datetime.fromisoformat(scheduled_date)
        
        db.session.add(campaign)
        db.session.commit()
        
        flash('Campaign created!', 'success')
        return redirect(url_for('marketing.view_campaign', campaign_id=campaign.id))
    
    # Get templates for selection
    email_templates = EmailTemplate.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).all()
    
    sms_templates = SMSTemplate.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).all()
    
    return render_template('marketing/create_campaign.html',
                         email_templates=email_templates,
                         sms_templates=sms_templates)


@bp.route('/campaigns/<int:campaign_id>')
@login_required
def view_campaign(campaign_id):
    """View campaign details."""
    campaign = MarketingCampaign.query.filter_by(
        id=campaign_id,
        trainer_id=current_user.id
    ).first_or_404()
    
    communications = CommunicationLog.query.filter_by(
        campaign_id=campaign.id
    ).order_by(CommunicationLog.sent_at.desc()).all()
    
    return render_template('marketing/view_campaign.html',
                         campaign=campaign,
                         communications=communications)


@bp.route('/campaigns/<int:campaign_id>/launch', methods=['POST'])
@login_required
def launch_campaign(campaign_id):
    """Launch marketing campaign."""
    campaign = MarketingCampaign.query.filter_by(
        id=campaign_id,
        trainer_id=current_user.id
    ).first_or_404()
    
    campaign.status = 'active'
    campaign.launched_at = datetime.utcnow()
    db.session.commit()
    
    # TODO: Implement actual campaign execution logic
    # This would integrate with Twilio/SendGrid to send messages
    
    flash(f'Campaign "{campaign.name}" launched!', 'success')
    return redirect(url_for('marketing.view_campaign', campaign_id=campaign.id))
