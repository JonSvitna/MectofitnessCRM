"""
Seed exercise library from WGER Workout Manager API.

This script fetches exercises from the free WGER API and populates
the ExerciseLibrary table with comprehensive exercise data.

WGER API: https://wger.de/api/v2/
License: Open source (AGPLv3+)
"""
import requests
import json
import time
from datetime import datetime
from app import create_app, db
from app.models.exercise_library import ExerciseLibrary

# WGER API endpoints
WGER_BASE_URL = "https://wger.de/api/v2"
LANGUAGE_ID = 2  # English

# Category mapping from WGER to our system
CATEGORY_MAPPING = {
    8: "strength",      # Arms
    10: "strength",     # Legs
    11: "strength",     # Chest
    12: "strength",     # Back
    13: "strength",     # Shoulders
    14: "strength",     # Abs
    9: "cardio",        # Cardio
}

# Difficulty mapping
DIFFICULTY_MAPPING = {
    1: "beginner",
    2: "intermediate",
    3: "advanced"
}

# Equipment mapping
EQUIPMENT_MAPPING = {
    1: "barbell",
    2: "sz-bar",
    3: "dumbbell",
    4: "gym mat",
    5: "swiss ball",
    6: "pull-up bar",
    7: "none (bodyweight)",
    8: "bench",
    9: "incline bench",
    10: "kettlebell",
}

# Muscle group mapping
MUSCLE_MAPPING = {
    1: "biceps",
    2: "anterior deltoid",
    3: "serratus anterior",
    4: "chest",
    5: "triceps",
    6: "abs",
    7: "calves",
    8: "glutes",
    9: "trapezius",
    10: "quads",
    11: "hamstrings",
    12: "lats",
    13: "middle back",
    14: "obliques",
    15: "soleus",
}


def fetch_wger_data(endpoint, params=None):
    """Fetch data from WGER API with pagination."""
    url = f"{WGER_BASE_URL}/{endpoint}/"
    all_results = []
    
    if params is None:
        params = {}
    
    params.setdefault('limit', 50)
    
    while url:
        print(f"Fetching: {url}")
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            all_results.extend(data.get('results', []))
            url = data.get('next')
            params = None  # Next URL already contains params
            
            # Be nice to the API
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
    
    return all_results


def get_exercise_description(exercise_id):
    """Fetch detailed exercise description."""
    try:
        url = f"{WGER_BASE_URL}/exercise/{exercise_id}/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None


def transform_wger_exercise(exercise_info):
    """Transform WGER exercise data to our ExerciseLibrary model."""
    
    # Get name and description from translations (English language=2)
    translations = exercise_info.get('translations', [])
    name = 'Unknown Exercise'
    description = ''
    
    # Find English translation (language ID = 2)
    for translation in translations:
        if translation.get('language') == 2:  # English
            name = translation.get('name', 'Unknown Exercise')
            description_html = translation.get('description', '')
            # Simple HTML tag removal (basic)
            import re
            description = re.sub('<[^<]+?>', '', description_html).strip()
            break
    
    # If no English translation, skip this exercise
    if name == 'Unknown Exercise':
        return None
    
    # Get category
    category_id = exercise_info.get('category', {}).get('id')
    category = CATEGORY_MAPPING.get(category_id, 'strength')
    
    # Get muscle groups
    primary_muscles = []
    secondary_muscles = []
    
    for muscle in exercise_info.get('muscles', []):
        muscle_name = MUSCLE_MAPPING.get(muscle['id'], muscle.get('name_en', muscle['name']))
        if muscle_name:
            primary_muscles.append(muscle_name)
    
    for muscle in exercise_info.get('muscles_secondary', []):
        muscle_name = MUSCLE_MAPPING.get(muscle['id'], muscle.get('name_en', muscle['name']))
        if muscle_name:
            secondary_muscles.append(muscle_name)
    
    # Get equipment
    equipment = []
    for equip in exercise_info.get('equipment', []):
        equip_name = EQUIPMENT_MAPPING.get(equip['id'], equip.get('name', 'unknown'))
        if equip_name and equip_name != 'unknown':
            equipment.append(equip_name)
    
    # Build exercise data
    exercise_data = {
        'name': name,
        'description': description[:500] if description else None,  # Limit length
        'category': category,
        'primary_muscle_groups': json.dumps(primary_muscles) if primary_muscles else None,
        'secondary_muscle_groups': json.dumps(secondary_muscles) if secondary_muscles else None,
        'equipment_required': json.dumps(equipment) if equipment else json.dumps(["none (bodyweight)"]),
        'difficulty_level': 'intermediate',  # Default since WGER doesn't provide this
        'exercise_type': 'compound' if len(primary_muscles) > 1 else 'isolation',
        'is_custom': False,
        'is_public': True,
        'is_active': True,
    }
    
    # Add images if available
    if exercise_info.get('images'):
        first_image = exercise_info['images'][0]
        if first_image.get('image'):
            exercise_data['image_url'] = first_image['image']
    
    # Add variations if available
    if exercise_info.get('variations'):
        exercise_data['alternative_exercises'] = json.dumps([exercise_info['variations']])
    
    return exercise_data


def seed_exercises():
    """Main function to seed exercises from WGER."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("SEEDING EXERCISE LIBRARY FROM WGER API")
        print("=" * 60)
        
        # Check if exercises already exist
        existing_count = ExerciseLibrary.query.filter_by(is_custom=False).count()
        
        if existing_count > 0:
            response = input(f"\n⚠️  Found {existing_count} existing exercises. Delete and re-seed? (yes/no): ")
            if response.lower() == 'yes':
                print("Deleting existing exercises...")
                ExerciseLibrary.query.filter_by(is_custom=False).delete()
                db.session.commit()
                print("✅ Cleared existing exercises")
            else:
                print("❌ Aborting. No changes made.")
                return
        
        print("\n📥 Fetching exercises from WGER API...")
        print("This may take a few minutes...\n")
        
        # Fetch exercise data using the exerciseinfo endpoint (has all data in one call)
        try:
            exercises_data = fetch_wger_data('exerciseinfo', {'language': LANGUAGE_ID})
            print(f"✅ Fetched {len(exercises_data)} exercises from WGER")
        except Exception as e:
            print(f"❌ Error fetching exercises: {e}")
            return
        
        # Transform and insert exercises
        print("\n📝 Processing and inserting exercises...")
        success_count = 0
        error_count = 0
        
        for idx, exercise_info in enumerate(exercises_data, 1):
            try:
                # Transform data
                exercise_data = transform_wger_exercise(exercise_info)
                
                # Skip if no English translation found
                if exercise_data is None:
                    continue
                
                # Check if exercise with this name already exists
                existing = ExerciseLibrary.query.filter_by(
                    name=exercise_data['name'],
                    is_custom=False
                ).first()
                
                if existing:
                    print(f"⏭️  Skipping duplicate: {exercise_data['name']}")
                    continue
                
                # Create exercise
                exercise = ExerciseLibrary(**exercise_data)
                db.session.add(exercise)
                
                success_count += 1
                
                # Commit in batches
                if success_count % 50 == 0:
                    db.session.commit()
                    print(f"✅ Inserted {success_count} exercises...")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error processing exercise {idx}: {e}")
                db.session.rollback()
                continue
        
        # Final commit
        try:
            db.session.commit()
            print(f"\n{'=' * 60}")
            print(f"✅ SEEDING COMPLETE!")
            print(f"{'=' * 60}")
            print(f"✅ Successfully inserted: {success_count} exercises")
            if error_count > 0:
                print(f"⚠️  Errors encountered: {error_count}")
            print(f"\n📊 Total exercises in library: {ExerciseLibrary.query.count()}")
            print(f"   - Standard exercises: {ExerciseLibrary.query.filter_by(is_custom=False).count()}")
            print(f"   - Custom exercises: {ExerciseLibrary.query.filter_by(is_custom=True).count()}")
            
            # Show category breakdown
            print(f"\n📋 Exercise breakdown by category:")
            categories = db.session.query(
                ExerciseLibrary.category,
                db.func.count(ExerciseLibrary.id)
            ).filter_by(is_custom=False).group_by(ExerciseLibrary.category).all()
            
            for cat, count in categories:
                print(f"   - {cat}: {count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error committing to database: {e}")


if __name__ == '__main__':
    seed_exercises()
