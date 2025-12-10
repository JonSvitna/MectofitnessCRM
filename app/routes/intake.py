"""Client intake form routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.client import Client
from app.models.intake import ClientIntake
from app.models.program import Program
from app.models.settings import TrainerSettings
from app.services.intake_flow_service import IntakeFlowService
from datetime import datetime
import json

bp = Blueprint('intake', __name__, url_prefix='/intake')


@bp.route('/')
@login_required
def list_intakes():
    """List all client intakes."""
    page = request.args.get('page', 1, type=int)
    intakes = ClientIntake.query.filter_by(
        trainer_id=current_user.id
    ).order_by(ClientIntake.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('intake/list.html', intakes=intakes)


@bp.route('/create/<int:client_id>', methods=['GET', 'POST'])
@login_required
def create_intake(client_id):
    """Create new client intake form."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        intake = ClientIntake(
            client_id=client.id,
            trainer_id=current_user.id,
            age=request.form.get('age', type=int),
            fitness_experience=request.form.get('fitness_experience'),
            current_activity_level=request.form.get('current_activity_level'),
            primary_goal=request.form.get('primary_goal'),
            target_timeline=request.form.get('target_timeline'),
            current_weight=request.form.get('current_weight', type=float),
            target_weight=request.form.get('target_weight', type=float),
            height_cm=request.form.get('height_cm', type=float),
            sessions_per_week=request.form.get('sessions_per_week', type=int),
            preferred_session_duration=request.form.get('preferred_session_duration', type=int),
            preferred_training_time=request.form.get('preferred_training_time'),
            training_location=request.form.get('training_location'),
            medical_conditions=request.form.get('medical_conditions'),
            injuries=request.form.get('injuries'),
            dietary_restrictions=request.form.get('dietary_restrictions'),
            motivation_level=request.form.get('motivation_level', type=int),
            status='pending',
            completed_at=datetime.utcnow()
        )
        
        # Handle equipment as JSON
        equipment = request.form.getlist('equipment')
        intake.set_available_equipment(equipment)
        
        # Handle secondary goals as JSON
        secondary_goals = request.form.getlist('secondary_goals')
        intake.set_secondary_goals(secondary_goals)
        
        db.session.add(intake)
        db.session.commit()
        
        flash(f'Intake form created for {client.full_name}!', 'success')
        return redirect(url_for('intake.view_intake', intake_id=intake.id))
    
    return render_template('intake/create.html', client=client)


@bp.route('/<int:intake_id>')
@login_required
def view_intake(intake_id):
    """View intake form details."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    return render_template('intake/view.html', intake=intake)


@bp.route('/<int:intake_id>/generate-program', methods=['POST'])
@login_required
def generate_program(intake_id):
    """Generate AI program from intake form."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    
    # Check if trainer has AI features enabled
    trainer_settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not trainer_settings or not trainer_settings.enable_ai_programs:
        flash('AI program generation is not enabled. Please enable it in settings.', 'warning')
        return redirect(url_for('intake.view_intake', intake_id=intake.id))
    
    # AI Program Generation Logic (placeholder for actual AI implementation)
    # This would call an AI service to generate a personalized program
    
    program_name = f"AI-Generated Program for {intake.client.full_name}"
    duration_weeks = 12  # Default
    
    # Adjust duration based on target timeline
    if intake.target_timeline == '4_weeks':
        duration_weeks = 4
    elif intake.target_timeline == '8_weeks':
        duration_weeks = 8
    elif intake.target_timeline == '12_weeks':
        duration_weeks = 12
    elif intake.target_timeline == '6_months':
        duration_weeks = 24
    
    program = Program(
        trainer_id=current_user.id,
        client_id=intake.client_id,
        name=program_name,
        description=f"AI-generated program based on intake assessment. Goal: {intake.primary_goal}",
        goal=intake.primary_goal,
        duration_weeks=duration_weeks,
        difficulty_level=intake.fitness_experience,
        is_ai_generated=True,
        ai_model_version='v1.0',
        status='active'
    )
    
    db.session.add(program)
    db.session.flush()
    
    # Link program to intake
    intake.ai_generated_program_id = program.id
    intake.status = 'program_assigned'
    intake.reviewed_at = datetime.utcnow()
    
    # Store AI recommendations
    recommendations = {
        'bmi': intake.calculate_bmi(),
        'recommended_sessions_per_week': intake.sessions_per_week or 3,
        'focus_areas': [intake.primary_goal],
        'considerations': []
    }
    
    if intake.medical_conditions:
        recommendations['considerations'].append('Medical conditions noted')
    if intake.injuries:
        recommendations['considerations'].append('Previous injuries noted')
    
    intake.ai_recommendations = json.dumps(recommendations)
    
    db.session.commit()
    
    flash(f'AI program generated successfully for {intake.client.full_name}!', 'success')
    return redirect(url_for('programs.view_program', program_id=program.id))


@bp.route('/<int:intake_id>/review', methods=['POST'])
@login_required
def review_intake(intake_id):
    """Mark intake as reviewed."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    
    intake.status = 'reviewed'
    intake.reviewed_at = datetime.utcnow()
    db.session.commit()
    
    flash('Intake form marked as reviewed!', 'success')
    return redirect(url_for('intake.view_intake', intake_id=intake.id))


@bp.route('/start/<int:client_id>', methods=['GET', 'POST'])
@login_required
def start_intake(client_id):
    """Start automated intake flow for a client."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        # Initialize intake flow service
        intake_service = IntakeFlowService()
        
        # Get trainer settings for branding
        trainer_settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
        trainer_name = current_user.full_name if current_user.full_name else "Your Trainer"
        business_name = trainer_settings.business_name if trainer_settings else "Mectofitn essCRM"
        
        # Send welcome email
        try:
            intake_service.send_welcome_email(
                client_email=client.email,
                client_name=client.full_name,
                trainer_name=trainer_name,
                business_name=business_name
            )
            
            # Send intake form request
            form_link = url_for('intake.client_form', client_id=client.id, _external=True)
            intake_service.send_intake_form_request(
                client_email=client.email,
                client_name=client.full_name,
                trainer_name=trainer_name,
                form_link=form_link
            )
            
            flash(f'Intake flow started! Welcome and intake form emails sent to {client.email}', 'success')
            return redirect(url_for('clients.view_client', client_id=client.id))
        except Exception as e:
            flash(f'Error sending emails: {str(e)}. Check your SendGrid configuration.', 'danger')
            return redirect(url_for('intake.start_intake', client_id=client.id))
    
    return render_template('intake/start.html', client=client)


@bp.route('/form/<int:client_id>', methods=['GET', 'POST'])
def client_form(client_id):
    """Client-facing intake form (no login required)."""
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'POST':
        # Create intake record
        intake = ClientIntake(
            client_id=client.id,
            trainer_id=client.trainer_id,
            age=request.form.get('age', type=int),
            gender=request.form.get('gender'),
            height_cm=request.form.get('height_cm', type=float),
            weight_kg=request.form.get('weight_kg', type=float),
            fitness_experience=request.form.get('fitness_experience'),
            primary_goal=request.form.get('primary_goal'),
            sessions_per_week=request.form.get('sessions_per_week', type=int),
            session_duration=request.form.get('session_duration', type=int),
            preferred_workout_time=request.form.get('preferred_workout_time'),
            workout_location=request.form.get('workout_location'),
            target_timeline=request.form.get('target_timeline'),
            medical_conditions=request.form.get('medical_conditions'),
            injuries=request.form.get('injuries'),
            dietary_restrictions=request.form.get('dietary_restrictions'),
            motivation_level=request.form.get('motivation_level', type=int),
            status='form_completed',
            completed_at=datetime.utcnow()
        )
        
        # Handle equipment and secondary goals
        equipment = request.form.getlist('equipment')
        intake.set_available_equipment(equipment)
        
        secondary_goals = request.form.getlist('secondary_goals')
        intake.set_secondary_goals(secondary_goals)
        
        db.session.add(intake)
        db.session.commit()
        
        # Send document signing request
        intake_service = IntakeFlowService()
        documents_link = url_for('intake.client_documents', intake_id=intake.id, _external=True)
        
        try:
            intake_service.send_document_signing_request(
                client_email=client.email,
                client_name=client.full_name,
                trainer_name=client.trainer.full_name if client.trainer else "Your Trainer",
                documents_link=documents_link
            )
        except Exception as e:
            print(f"Error sending document email: {e}")
        
        return redirect(url_for('intake.form_success', client_id=client.id))
    
    return render_template('intake/form.html', client=client)


@bp.route('/form-success/<int:client_id>')
def form_success(client_id):
    """Intake form submission success page."""
    client = Client.query.get_or_404(client_id)
    return render_template('intake/form_success.html', client=client)


@bp.route('/documents/<int:intake_id>', methods=['GET', 'POST'])
def client_documents(intake_id):
    """Client-facing document signing interface."""
    intake = ClientIntake.query.get_or_404(intake_id)
    
    if request.method == 'POST':
        # Store signature and mark documents as signed
        signature = request.form.get('signature')
        intake.documents_signed = True
        intake.signature_data = signature
        intake.status = 'documents_signed'
        db.session.commit()
        
        # Send photo upload request
        intake_service = IntakeFlowService()
        photos_link = url_for('intake.client_photos', intake_id=intake.id, _external=True)
        
        try:
            intake_service.send_photo_upload_request(
                client_email=intake.client.email,
                client_name=intake.client.full_name,
                trainer_name=intake.client.trainer.full_name if intake.client.trainer else "Your Trainer",
                upload_link=photos_link
            )
        except Exception as e:
            print(f"Error sending photo email: {e}")
        
        return redirect(url_for('intake.documents_success', intake_id=intake.id))
    
    # Get document templates
    intake_service = IntakeFlowService()
    waiver = intake_service.generate_liability_waiver(
        client_name=intake.client.full_name,
        business_name="MectofitnessCRM",
        date=datetime.utcnow().strftime('%B %d, %Y')
    )
    parq = intake_service.generate_parq_form(
        client_name=intake.client.full_name,
        date=datetime.utcnow().strftime('%B %d, %Y')
    )
    
    return render_template('intake/documents.html', intake=intake, waiver=waiver, parq=parq)


@bp.route('/documents-success/<int:intake_id>')
def documents_success(intake_id):
    """Document signing success page."""
    intake = ClientIntake.query.get_or_404(intake_id)
    return render_template('intake/documents_success.html', intake=intake)


@bp.route('/photos/<int:intake_id>', methods=['GET', 'POST'])
def client_photos(intake_id):
    """Client-facing photo upload interface."""
    intake = ClientIntake.query.get_or_404(intake_id)
    
    if request.method == 'POST':
        # Handle photo uploads (placeholder - implement file storage)
        intake.photos_uploaded = True
        intake.status = 'completed'
        db.session.commit()
        
        flash('Photos uploaded successfully! Your intake process is complete.', 'success')
        return redirect(url_for('intake.photos_success', intake_id=intake.id))
    
    return render_template('intake/photos.html', intake=intake)


@bp.route('/photos-success/<int:intake_id>')
def photos_success(intake_id):
    """Photo upload success page."""
    intake = ClientIntake.query.get_or_404(intake_id)
    return render_template('intake/photos_success.html', intake=intake)
