#!/usr/bin/env python3
"""
Quick diagnostic script to check exercise library status.
Run this to see if exercises are in the database.
"""
from app import create_app, db
from app.models.exercise_library import ExerciseLibrary
from sqlalchemy import func

def main():
    app = create_app()

    with app.app_context():
        print("=" * 70)
        print("EXERCISE LIBRARY DIAGNOSTIC")
        print("=" * 70)

        # Total counts
        total = ExerciseLibrary.query.count()
        active = ExerciseLibrary.query.filter_by(is_active=True).count()
        custom = ExerciseLibrary.query.filter_by(is_custom=True, is_active=True).count()
        standard = ExerciseLibrary.query.filter_by(is_custom=False, is_active=True).count()

        print(f"\n📊 EXERCISE COUNTS:")
        print(f"   Total exercises in database: {total}")
        print(f"   Active exercises: {active}")
        print(f"   Standard exercises (from WGER): {standard}")
        print(f"   Custom exercises: {custom}")

        if active == 0:
            print(f"\n⚠️  WARNING: No active exercises found!")
            print(f"   The exercise library will appear empty.")
            print(f"\n💡 SOLUTION:")
            print(f"   Run the seed script to populate exercises:")
            print(f"   $ python seed_exercises.py")
            return

        # Category breakdown
        categories = db.session.query(
            ExerciseLibrary.category,
            func.count(ExerciseLibrary.id)
        ).filter_by(is_active=True).group_by(ExerciseLibrary.category).all()

        if categories:
            print(f"\n📋 BREAKDOWN BY CATEGORY:")
            for cat, count in categories:
                if cat:
                    print(f"   - {cat.capitalize()}: {count} exercises")

        # Difficulty breakdown
        difficulties = db.session.query(
            ExerciseLibrary.difficulty_level,
            func.count(ExerciseLibrary.id)
        ).filter_by(is_active=True).group_by(ExerciseLibrary.difficulty_level).all()

        if difficulties:
            print(f"\n⚡ BREAKDOWN BY DIFFICULTY:")
            for diff, count in difficulties:
                if diff:
                    print(f"   - {diff.capitalize()}: {count} exercises")

        # Equipment breakdown (limited to top 5)
        print(f"\n🏋️  EQUIPMENT AVAILABLE:")
        exercises = ExerciseLibrary.query.filter_by(is_active=True).limit(100).all()
        equipment_set = set()
        for ex in exercises:
            equipment_set.update(ex.get_equipment())

        equipment_list = sorted(list(equipment_set))[:10]
        if equipment_list:
            for equip in equipment_list:
                print(f"   - {equip}")
            if len(equipment_set) > 10:
                print(f"   ... and {len(equipment_set) - 10} more")

        # Sample exercises
        print(f"\n🎯 SAMPLE EXERCISES:")
        samples = ExerciseLibrary.query.filter_by(is_active=True).limit(5).all()
        for ex in samples:
            muscles = ex.get_primary_muscles()
            muscle_str = ', '.join(muscles[:2]) if muscles else 'N/A'
            print(f"   - {ex.name} ({ex.category}) - {muscle_str}")

        print(f"\n✅ DIAGNOSIS COMPLETE")
        print(f"   Exercise library has {active} active exercises")
        print(f"   Filters should be working correctly")
        print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\nMake sure:")
        print(f"   1. Database is properly configured (check .env)")
        print(f"   2. Flask dependencies are installed (pip install -r requirements.txt)")
        print(f"   3. Database migrations are up to date")
