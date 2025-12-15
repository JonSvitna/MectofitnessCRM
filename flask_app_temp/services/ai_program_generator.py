"""AI-powered training program generator using OpenAI."""
import os
import json
import openai
from typing import Dict, List, Optional
from app.models.exercise_library import ExerciseLibrary
from app import db


class AIProgramGenerator:
    """Generate personalized training programs using AI."""
    
    def __init__(self):
        """Initialize the AI program generator."""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        self.model = "gpt-4-turbo-preview"  # or gpt-3.5-turbo for cheaper/faster
    
    def is_available(self) -> bool:
        """Check if AI service is available."""
        return bool(self.api_key)
    
    def generate_program(
        self,
        client_info: Dict,
        program_goal: str,
        duration_weeks: int,
        difficulty_level: str,
        equipment_available: Optional[List[str]] = None,
        training_frequency: int = 3
    ) -> Dict:
        """
        Generate a complete training program using AI.
        
        Args:
            client_info: Dictionary with client details (name, fitness_level, medical_conditions, etc.)
            program_goal: Training goal (e.g., "Build muscle", "Weight loss")
            duration_weeks: Program duration in weeks
            difficulty_level: beginner, intermediate, or advanced
            equipment_available: List of available equipment
            training_frequency: Sessions per week
            
        Returns:
            Dictionary with program structure and exercises
        """
        if not self.is_available():
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        
        # Get available exercises from database
        available_exercises = self._get_available_exercises(equipment_available, difficulty_level)
        
        # Build the prompt
        prompt = self._build_program_prompt(
            client_info,
            program_goal,
            duration_weeks,
            difficulty_level,
            equipment_available,
            training_frequency,
            available_exercises
        )
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert personal trainer and strength & conditioning coach with 15+ years of experience. 
                        You create scientifically-backed, personalized training programs that are safe, effective, and progressive.
                        Always consider the client's fitness level, goals, and any medical conditions.
                        Your programs should include proper warm-ups, progressive overload, and adequate recovery."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content
            program_data = self._parse_ai_response(ai_response)
            
            return {
                "success": True,
                "program_data": program_data,
                "ai_model": self.model,
                "raw_response": ai_response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate program with AI. Please try again."
            }
    
    def _get_available_exercises(
        self,
        equipment: Optional[List[str]],
        difficulty_level: str
    ) -> List[Dict]:
        """Get relevant exercises from the database."""
        query = ExerciseLibrary.query.filter_by(is_active=True)
        
        # Filter by difficulty if needed
        if difficulty_level:
            query = query.filter(
                (ExerciseLibrary.difficulty_level == difficulty_level) |
                (ExerciseLibrary.difficulty_level == None)
            )
        
        # Get a diverse set of exercises (limit for prompt size)
        exercises = query.limit(100).all()
        
        exercise_list = []
        for ex in exercises:
            exercise_list.append({
                "id": ex.id,
                "name": ex.name,
                "category": ex.category,
                "difficulty": ex.difficulty_level,
                "primary_muscles": ex.get_primary_muscles(),
                "equipment": ex.get_equipment(),
                "description": ex.description[:100] if ex.description else ""
            })
        
        return exercise_list
    
    def _build_program_prompt(
        self,
        client_info: Dict,
        program_goal: str,
        duration_weeks: int,
        difficulty_level: str,
        equipment_available: Optional[List[str]],
        training_frequency: int,
        available_exercises: List[Dict]
    ) -> str:
        """Build the prompt for AI program generation."""
        
        equipment_str = ", ".join(equipment_available) if equipment_available else "Full gym access"
        
        prompt = f"""Create a {duration_weeks}-week personalized training program with the following specifications:

CLIENT PROFILE:
- Name: {client_info.get('name', 'Client')}
- Fitness Level: {client_info.get('fitness_level', difficulty_level)}
- Primary Goal: {program_goal}
- Training Frequency: {training_frequency} sessions per week
- Available Equipment: {equipment_str}
"""
        
        if client_info.get('medical_conditions'):
            prompt += f"- Medical Considerations: {client_info['medical_conditions']}\n"
        
        prompt += f"""
PROGRAM REQUIREMENTS:
1. Create a {training_frequency}-day split appropriate for the goal and fitness level
2. Each workout should take 45-75 minutes
3. Include proper warm-up and cool-down
4. Progressive overload built into the program
5. Select exercises from the available exercise library (provided below)
6. Specify sets, reps, rest periods, and tempo where appropriate
7. Include exercise notes for proper form and safety

EXERCISE LIBRARY (Sample of {len(available_exercises)} exercises):
"""
        
        # Add sample of exercises to prompt
        for i, ex in enumerate(available_exercises[:30]):  # Limit to 30 for prompt size
            prompt += f"\n{i+1}. {ex['name']} - {ex['category']}"
            if ex['primary_muscles']:
                prompt += f" ({', '.join(ex['primary_muscles'])})"
            if ex['equipment']:
                prompt += f" [Equipment: {', '.join(ex['equipment'])}]"
        
        prompt += f"""

OUTPUT FORMAT (Return as JSON):
{{
    "program_overview": "Brief program description and strategy",
    "training_split": "e.g., Push/Pull/Legs or Upper/Lower/Full Body",
    "weeks": [
        {{
            "week_number": 1,
            "focus": "Week focus/theme",
            "workouts": [
                {{
                    "day": 1,
                    "title": "Workout title",
                    "duration_minutes": 60,
                    "exercises": [
                        {{
                            "exercise_name": "Exercise from library",
                            "exercise_id": ID from library or null if custom,
                            "sets": 3,
                            "reps": "10-12",
                            "rest_seconds": 90,
                            "tempo": "2-0-2-0",
                            "notes": "Form cues and tips"
                        }}
                    ]
                }}
            ]
        }}
    ],
    "progression_notes": "How to progress through the program",
    "nutrition_tips": "Brief nutrition guidance for the goal",
    "recovery_tips": "Recovery and rest day guidance"
}}

Create a complete, scientifically-sound program that will help the client achieve their goal safely and effectively.
"""
        
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse the AI response into structured data."""
        try:
            # Try to extract JSON from the response
            # Sometimes AI wraps JSON in markdown code blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            # Parse JSON
            program_data = json.loads(json_str)
            return program_data
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response
            return {
                "program_overview": response,
                "raw": True,
                "error": "Could not parse structured program data"
            }
    
    def save_program_to_database(
        self,
        program_id: int,
        program_data: Dict
    ):
        """Save the AI-generated program to the database."""
        from app.models.program import Program, Exercise
        
        program = Program.query.get(program_id)
        if not program:
            raise ValueError(f"Program {program_id} not found")
        
        # Update program metadata
        program.is_ai_generated = True
        program.ai_model_version = self.model
        program.program_data = json.dumps(program_data)
        
        # Clear existing exercises
        Exercise.query.filter_by(program_id=program_id).delete()
        
        # Add exercises from AI program
        if "weeks" in program_data:
            for week in program_data["weeks"]:
                if "workouts" in week:
                    for workout in week["workouts"]:
                        day_number = workout.get("day", 1)
                        
                        for idx, ex_data in enumerate(workout.get("exercises", [])):
                            exercise = Exercise(
                                program_id=program_id,
                                day_number=day_number,
                                order_in_day=idx + 1,
                                name=ex_data.get("exercise_name"),
                                sets=ex_data.get("sets"),
                                reps=ex_data.get("reps"),
                                rest_seconds=ex_data.get("rest_seconds"),
                                notes=ex_data.get("notes", ""),
                                exercise_library_id=ex_data.get("exercise_id")
                            )
                            db.session.add(exercise)
        
        db.session.commit()
        return program
