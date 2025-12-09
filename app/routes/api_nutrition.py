"""RESTful API for nutrition - meal plans and food logging."""
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
import json
from app import db
from app.models.nutrition import NutritionPlan, FoodLog
from app.models.client import Client

api_nutrition = Blueprint('api_nutrition', __name__, url_prefix='/api/v1/nutrition')

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

@api_nutrition.route('/plans', methods=['GET'])
@login_required
def get_nutrition_plans():
    """Get nutrition plans."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        client_id = request.args.get('client_id', type=int)
        status = request.args.get('status')
        
        query = NutritionPlan.query.filter_by(trainer_id=current_user.id)
        if client_id:
            query = query.filter_by(client_id=client_id)
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(NutritionPlan.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        plans = [{
            'id': p.id, 'client_id': p.client_id, 'plan_name': p.plan_name,
            'status': p.status, 'start_date': p.start_date.isoformat() if p.start_date else None,
            'end_date': p.end_date.isoformat() if p.end_date else None,
            'daily_calories': p.daily_calories, 'protein_grams': p.protein_grams,
            'carbs_grams': p.carbs_grams, 'fat_grams': p.fat_grams,
            'dietary_preferences': p.dietary_preferences, 'created_at': p.created_at.isoformat()
        } for p in pagination.items]
        
        return success_response({'plans': plans, 'pagination': {
            'page': pagination.page, 'per_page': pagination.per_page,
            'total_pages': pagination.pages, 'total_items': pagination.total
        }})
    except Exception as e:
        return error_response(f'Error fetching plans: {str(e)}', 500)

@api_nutrition.route('/plans/<int:plan_id>', methods=['GET'])
@login_required
def get_nutrition_plan(plan_id):
    """Get detailed nutrition plan with meal plan."""
    try:
        plan = NutritionPlan.query.get(plan_id)
        if not plan or plan.trainer_id != current_user.id:
            return error_response('Plan not found', 404)
        
        return success_response({
            'id': plan.id, 'client_id': plan.client_id, 'plan_name': plan.plan_name,
            'status': plan.status, 'start_date': plan.start_date.isoformat() if plan.start_date else None,
            'end_date': plan.end_date.isoformat() if plan.end_date else None,
            'daily_calories': plan.daily_calories, 'protein_grams': plan.protein_grams,
            'carbs_grams': plan.carbs_grams, 'fat_grams': plan.fat_grams,
            'meal_plan': plan.get_meal_plan(), 'dietary_preferences': plan.dietary_preferences,
            'foods_to_avoid': plan.foods_to_avoid, 'supplements': plan.supplements,
            'hydration_target_ml': plan.hydration_target_ml, 'notes': plan.notes,
            'created_at': plan.created_at.isoformat(), 'updated_at': plan.updated_at.isoformat()
        })
    except Exception as e:
        return error_response(f'Error fetching plan: {str(e)}', 500)

@api_nutrition.route('/plans', methods=['POST'])
@login_required
def create_nutrition_plan():
    """Create a new nutrition plan."""
    try:
        data = request.get_json()
        if not data or not data.get('client_id'):
            return error_response('client_id is required')
        
        client = Client.query.get(data['client_id'])
        if not client or client.trainer_id != current_user.id:
            return error_response('Invalid client_id', 403)
        
        plan = NutritionPlan(
            client_id=data['client_id'], trainer_id=current_user.id,
            plan_name=data.get('plan_name', f'Plan for {client.first_name}'),
            status=data.get('status', 'draft'),
            start_date=date.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=date.fromisoformat(data['end_date']) if data.get('end_date') else None,
            daily_calories=data.get('daily_calories'),
            protein_grams=data.get('protein_grams'),
            carbs_grams=data.get('carbs_grams'),
            fat_grams=data.get('fat_grams'),
            meal_plan_data=json.dumps(data.get('meal_plan', {})),
            dietary_preferences=data.get('dietary_preferences'),
            foods_to_avoid=data.get('foods_to_avoid'),
            supplements=data.get('supplements'),
            hydration_target_ml=data.get('hydration_target_ml'),
            notes=data.get('notes')
        )
        db.session.add(plan)
        db.session.commit()
        
        return success_response({'id': plan.id, 'plan_name': plan.plan_name},
                              'Nutrition plan created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating plan: {str(e)}', 500)

@api_nutrition.route('/plans/<int:plan_id>', methods=['PUT', 'PATCH'])
@login_required
def update_nutrition_plan(plan_id):
    """Update a nutrition plan."""
    try:
        plan = NutritionPlan.query.get(plan_id)
        if not plan or plan.trainer_id != current_user.id:
            return error_response('Plan not found', 404)
        
        data = request.get_json()
        fields = ['plan_name', 'status', 'daily_calories', 'protein_grams', 'carbs_grams',
                 'fat_grams', 'dietary_preferences', 'foods_to_avoid', 'supplements',
                 'hydration_target_ml', 'notes']
        for field in fields:
            if field in data:
                setattr(plan, field, data[field])
        
        if 'start_date' in data:
            plan.start_date = date.fromisoformat(data['start_date']) if data['start_date'] else None
        if 'end_date' in data:
            plan.end_date = date.fromisoformat(data['end_date']) if data['end_date'] else None
        if 'meal_plan' in data:
            plan.meal_plan_data = json.dumps(data['meal_plan'])
        
        plan.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': plan.id}, 'Plan updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating plan: {str(e)}', 500)

@api_nutrition.route('/plans/<int:plan_id>', methods=['DELETE'])
@login_required
def delete_nutrition_plan(plan_id):
    """Delete a nutrition plan."""
    try:
        plan = NutritionPlan.query.get(plan_id)
        if not plan or plan.trainer_id != current_user.id:
            return error_response('Plan not found', 404)
        
        db.session.delete(plan)
        db.session.commit()
        return success_response(message='Plan deleted')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting plan: {str(e)}', 500)

@api_nutrition.route('/logs', methods=['GET'])
@login_required
def get_food_logs():
    """Get food logs."""
    try:
        client_id = request.args.get('client_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        meal_type = request.args.get('meal_type')
        
        query = FoodLog.query.filter_by(trainer_id=current_user.id)
        if client_id:
            query = query.filter_by(client_id=client_id)
        if start_date:
            query = query.filter(FoodLog.log_date >= date.fromisoformat(start_date))
        if end_date:
            query = query.filter(FoodLog.log_date <= date.fromisoformat(end_date))
        if meal_type:
            query = query.filter_by(meal_type=meal_type)
        
        logs = query.order_by(FoodLog.log_date.desc(), FoodLog.meal_time.desc()).limit(200).all()
        
        return success_response({'logs': [{
            'id': l.id, 'client_id': l.client_id, 'log_date': l.log_date.isoformat(),
            'meal_time': l.meal_time.strftime('%H:%M') if l.meal_time else None,
            'meal_type': l.meal_type, 'food_name': l.food_name, 'serving_size': l.serving_size,
            'calories': l.calories, 'protein_grams': l.protein_grams,
            'carbs_grams': l.carbs_grams, 'fat_grams': l.fat_grams,
            'photo_url': l.photo_url, 'created_at': l.created_at.isoformat()
        } for l in logs]})
    except Exception as e:
        return error_response(f'Error fetching logs: {str(e)}', 500)

@api_nutrition.route('/logs', methods=['POST'])
@login_required
def create_food_log():
    """Create a new food log entry."""
    try:
        data = request.get_json()
        if not data or not data.get('client_id') or not data.get('food_name'):
            return error_response('client_id and food_name are required')
        
        client = Client.query.get(data['client_id'])
        if not client or client.trainer_id != current_user.id:
            return error_response('Invalid client_id', 403)
        
        log = FoodLog(
            client_id=data['client_id'], trainer_id=current_user.id,
            log_date=date.fromisoformat(data.get('log_date', str(date.today()))),
            meal_time=datetime.strptime(data['meal_time'], '%H:%M').time() if data.get('meal_time') else None,
            meal_type=data.get('meal_type'),
            food_name=data['food_name'],
            serving_size=data.get('serving_size'),
            calories=data.get('calories'),
            protein_grams=data.get('protein_grams'),
            carbs_grams=data.get('carbs_grams'),
            fat_grams=data.get('fat_grams'),
            fiber_grams=data.get('fiber_grams'),
            photo_url=data.get('photo_url'),
            notes=data.get('notes')
        )
        db.session.add(log)
        db.session.commit()
        
        return success_response({'id': log.id, 'log_date': log.log_date.isoformat()},
                              'Food log created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating log: {str(e)}', 500)

@api_nutrition.route('/logs/summary/<int:client_id>', methods=['GET'])
@login_required
def get_nutrition_summary(client_id):
    """Get nutrition summary for a client."""
    try:
        client = Client.query.get(client_id)
        if not client or client.trainer_id != current_user.id:
            return error_response('Client not found', 404)
        
        target_date = request.args.get('date', str(date.today()))
        target = date.fromisoformat(target_date)
        
        logs = FoodLog.query.filter(
            FoodLog.client_id == client_id,
            FoodLog.log_date == target
        ).all()
        
        totals = {
            'date': target.isoformat(),
            'total_calories': sum(l.calories or 0 for l in logs),
            'total_protein': sum(l.protein_grams or 0 for l in logs),
            'total_carbs': sum(l.carbs_grams or 0 for l in logs),
            'total_fat': sum(l.fat_grams or 0 for l in logs),
            'meal_count': len(logs)
        }
        
        active_plan = NutritionPlan.query.filter(
            NutritionPlan.client_id == client_id,
            NutritionPlan.status == 'active'
        ).first()
        
        if active_plan:
            totals['target_calories'] = active_plan.daily_calories
            totals['target_protein'] = active_plan.protein_grams
            totals['target_carbs'] = active_plan.carbs_grams
            totals['target_fat'] = active_plan.fat_grams
        
        return success_response(totals)
    except Exception as e:
        return error_response(f'Error calculating summary: {str(e)}', 500)
